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
    
    obs, info = meta_env.reset()
    [print(observation) for observation in obs]
    [print(inf) for inf in info]


    done = [False] * meta_env.n_envs
    while not all(done):
        actions = [env.action_space.sample() for env in meta_env.envs]
        obs, rewards, terminateds, truncateds, infos = meta_env.step(actions)
        done = [t or tr for t, tr in zip(terminateds, truncateds)]


if __name__ == "__main__":
    main()