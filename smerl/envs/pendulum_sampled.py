import random
import gymnasium as gym
import numpy as np

from smerl.utils.aux import print_info


class PendulumSampledMetaEnv(gym.Env):
    """
    Meta Pendulum environment with sampled transitions.
    """

    def __init__(self, gravities):
        """
        Class constructor for PendulumSampledMetaEnv.
        Args:
            gravities (list): List of gravitational constants for each environment.
        """

        self.n_envs = len(gravities)
        self.gravities = gravities

        # Initialize multiple environments
        self.envs = self._init_envs()

    def reset(self):
        """
        Resets all environments and returns a sampled observation and info.
        """

        # Reset all environments and collect initial observations
        obs, infos = [], []

        for i, env in enumerate(self.envs):
            observation, info = env.reset()
            obs.append(observation)
            info['gravity'] = self.gravities[i]
            infos.append(info)

        # Return sampled observation and info
        n_rand = random.randint(0, self.n_envs - 1)

        return obs[n_rand], infos[n_rand]

    def step(self, actions):
        """
        Steps through a random environment.
        """

        obs = []
        rewards = []
        terminateds = []
        truncateds = []
        infos = []

        for i, (env, action) in enumerate(zip(self.envs, actions)):
            print(action)
            o, r, term, trunc, info = env.step(action)
            info['gravity'] = self.gravities[i]

            obs.append(o)
            rewards.append(r)
            terminateds.append(term)
            truncateds.append(trunc)
            infos.append(info)

        # Randomly select one environment's results
        n_rand = random.randint(0, self.n_envs - 1)
        print_info(f'Pendulum environment with gravity {self.gravities[n_rand]}. Reward received: {rewards[n_rand]}.')
        
        terminated = any(terminateds)
        truncated = any(truncateds)

        return obs[n_rand], rewards[n_rand], terminated, truncated, infos[n_rand]

    def render():
        raise NotImplementedError("Render method is not implemented.")

    def close(self):
        """
        Closes all the environments.
        """
        for env in self.envs:
            env.close()

    def _init_envs(self):
        """
        Initializes multiple environments with specified gravitational constants.
        Returns:
            list: List of initialized environments.
        """
        envs = []
        for gravity in self.gravities:
            envs.append(gym.make('Pendulum-v1', g=gravity))
            print_info(f'Pendulum environment with gravity {gravity} has been created.')

        return envs
