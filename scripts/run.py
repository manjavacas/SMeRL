import gymnasium as gym
from smerl.envs.sinergym import SinergymMetaEnv

def main():
    # Create meta environment
    env = SinergymMetaEnv(n_envs=2)

    obs, info = env.reset()

    print("Observation:", obs)
    print("Info:", info)


if __name__ == "__main__":
    main()