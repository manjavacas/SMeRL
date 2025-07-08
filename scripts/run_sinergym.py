import gymnasium as gym

from smerl.envs.sinergym import SinergymMetaEnv

def main():

    env_ids = [
        'Eplus-5zone-hot-continuous-stochastic-v1',
        'Eplus-5zone-cool-continuous-stochastic-v1',
        'Eplus-5zone-mixed-continuous-stochastic-v1'
    ]

    # Create meta environment
    meta_env = SinergymMetaEnv(env_ids)
    
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