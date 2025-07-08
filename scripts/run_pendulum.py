import os
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import gymnasium as gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import DummyVecEnv

from smerl.envs.pendulum import PendulumMetaEnv


def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    import torch
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def make_env(gravities):
    def _init():
        return PendulumMetaEnv(gravities)
    return _init


def format_gravity(g):
    return str(g).replace(".", "p")


def train_ppo(train_gravities, model_path, total_timesteps=500_000):
    env = DummyVecEnv([make_env(train_gravities)])
    model = PPO("MlpPolicy", env, verbose=0, device="cpu")
    model.learn(total_timesteps=total_timesteps)
    model.save(model_path)
    env.close()


def evaluate_on_gravity(gravity, model_path, episodes=20):
    test_env = PendulumMetaEnv([gravity])
    model = PPO.load(model_path)

    rewards = []

    for _ in range(episodes):
        obs, info = test_env.reset()
        done = False
        total_reward = 0.0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = test_env.step(action)
            done = terminated or truncated
            total_reward += reward

        rewards.append(total_reward)

    test_env.close()
    return np.mean(rewards), np.std(rewards)


def evaluate_all_agents(test_gravities, train_gravities, episodes=20):
    results = {}
    stds = {}

    print("\nEvaluating META-agent...\n")
    meta_means = []
    meta_stds = []
    for g in test_gravities:
        mean, std = evaluate_on_gravity(g, "models/ppo_meta", episodes)
        meta_means.append(mean)
        meta_stds.append(std)
        print(f"[META] Gravity {g:.2f} → Mean: {mean:.2f}, Std: {std:.2f}")
    results["Meta-agent"] = meta_means
    stds["Meta-agent"] = meta_stds

    for g_train in train_gravities:
        agent_name = f"Agent {g_train}"
        model_file = f"models/ppo_g_{format_gravity(g_train)}"
        means = []
        agent_stds = []
        for g_test in test_gravities:
            mean, std = evaluate_on_gravity(g_test, model_file, episodes)
            means.append(mean)
            agent_stds.append(std)
            print(
                f"[{agent_name}] → Test {g_test:.2f} → Mean: {mean:.2f}, Std: {std:.2f}")
        results[agent_name] = means
        stds[agent_name] = agent_stds

    return results, stds


def plot_results(results, stds, test_gravities, output_path):
    plt.figure(figsize=(14, 8))
    x = np.arange(len(test_gravities))
    width = 0.12

    for i, (agent, means) in enumerate(results.items()):
        error = stds[agent]
        plt.bar(x + i * width, means, width=width,
                yerr=error, capsize=5, label=agent)

    plt.xticks(x + width * (len(results) - 1) / 2,
               [f"{g:.2f}" for g in test_gravities], rotation=45)
    plt.xlabel("Unseen Gravity (m/s²)")
    plt.ylabel("Average Reward")
    plt.title("Performance of PPO Agents on Unseen Gravities")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nPlot saved to: {output_path}")


def save_results_csv(results, test_gravities, output_file):
    df = pd.DataFrame(results, index=[f"{g:.2f}" for g in test_gravities])
    df.index.name = "Gravity"
    df.to_csv(output_file)
    print(f"CSV saved to: {output_file}")


if __name__ == "__main__":
    set_seed(42)

    # Moon, Mars, Earth, etc.
    train_gravities = [1.62, 3.71, 9.81, 12.0, 15.0, 24.79]
    test_gravities = np.round(np.linspace(0.5, 26.0, 16), 2).tolist()

    total_timesteps = 150_000
    episodes = 20

    os.makedirs("models", exist_ok=True)

    print("Training META-agent...")
    train_ppo(train_gravities, model_path="models/ppo_meta",
              total_timesteps=total_timesteps)

    for g in train_gravities:
        model_name = f"ppo_g_{format_gravity(g)}"
        print(f"Training single-gravity agent for g = {g}...")
        train_ppo(
            [g], model_path=f"models/{model_name}", total_timesteps=total_timesteps)

    results, stds = evaluate_all_agents(
        test_gravities, train_gravities, episodes=episodes)

    plot_results(results, stds, test_gravities,
                 "results/pendulum_meta_comparison.png")
    save_results_csv(results, test_gravities,
                     "results/pendulum_meta_comparison.csv")

    csv_path = "results/pendulum_meta_comparison.csv"
    df = pd.read_csv(csv_path, index_col="Gravity")

    summary_stats = df.describe().T[["mean", "std", "min", "max", "50%"]]
    summary_stats.rename(columns={"50%": "median"}, inplace=True)

    summary_stats = summary_stats.sort_values(by="mean", ascending=False)

    print("\n=== General stats per agent ===\n")
    print(summary_stats.round(2))

    meta_rewards = df["Meta-agent"]
    relative_advantages = {}

    for agent in df.columns:
        if agent == "Meta-agent":
            continue
        relative = meta_rewards - df[agent]
        relative_advantages[agent] = {
            "mean_advantage": relative.mean(),
            "median_advantage": relative.median(),
            # cuántas veces gana el meta-agente
            "positive_cases": (relative > 0).sum(),
            "total": len(relative)
        }

    print("\n=== Meta agent advantage ===\n")
    for agent, stats in relative_advantages.items():
        win_ratio = stats["positive_cases"] / stats["total"]
        print(f"{agent}: Mean Advantage = {stats['mean_advantage']:.2f}, "
              f"Median = {stats['median_advantage']:.2f}, "
              f"Meta Wins = {win_ratio*100:.1f}% of test gravities")

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df)
    plt.xticks(rotation=45)
    plt.title("Rewards per agent (unseen gravities)")
    plt.ylabel("Reward")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("results/agent_reward_distributions.png", dpi=300)
    plt.close()
    print("\nGráfico guardado en: results/agent_reward_distributions.png")
