import gymnasium as gym
import numpy as np

from smerl.envs.pendulum_sampled import PendulumSampledMetaEnv

def main():

    gravities = [
        9.81,
        1.62,
        24.79
    ]

    n_envs = len(gravities)

    # Create meta environment
    meta_env = PendulumSampledMetaEnv(gravities)
    
    for ep in range(3):
        # Reset the environment
        obs, info = meta_env.reset()
        print(f"Episode {ep + 1} - Initial observation: {obs}, Info: {info}")

        done = False
        while not done:
            actions = [np.random.uniform(low=-2.0, high=2.0, size=(1,)) for _ in range(n_envs)]
            o, r, term, trunc, info = meta_env.step(actions)
            done = term or trunc
        

    meta_env.close()


if __name__ == "__main__":
    main()