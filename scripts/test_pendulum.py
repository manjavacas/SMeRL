import gymnasium as gym

from smerl.envs.pendulum import PendulumMetaEnv

def main():

    gravities = [
        9.81,
        1.62,
        24.79
    ]

    # Create meta environment
    meta_env = PendulumMetaEnv(gravities)
    
    for ep in range(3):

        done = [False] * meta_env.n_envs
        _, _ = meta_env.reset()

        while not all(done):
            actions = [env.action_space.sample() for env in meta_env.envs]
            obs, rewards, terminateds, truncateds, infos = meta_env.step(actions)
            done = [t or tr for t, tr in zip(terminateds, truncateds)]

    meta_env.close()


if __name__ == "__main__":
    main()