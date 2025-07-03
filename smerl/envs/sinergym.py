import gymnasium as gym
import numpy as np

import sinergym

from smerl.utils.aux import print_info


class SinergymMetaEnv(gym.Env):
    """
    Meta Sinergym environment.
    """

    def __init__(self, env_ids):
        """
        Class constructor for SinergymMetaEnv.
        """

        self.env_ids = env_ids
        self.n_envs = len(env_ids)

        self.envs = None

    def reset(self):
        """
        Resets all Sinergym environments and returns initial observations and infos.
        Returns:
            obs (list): List of initial observations from each environment.
            infos (list): List of info dictionaries from each environment.
        """

        # Initialize multiple Sinergym environments
        self.envs = self._init_envs()

        # Reset all environments and collect initial observations
        obs = []
        infos = []
        for env in self.envs:
            observation, info = env.reset()
            obs.append(observation)
            info['env_id'] = env.spec.id if env.spec else 'unknown'
            infos.append(info)

        return obs, infos

    def step(self, actions):
        """
        Steps through all environments with the provided actions.
        Args:
            actions (list): List of actions for each environment.
        Returns:
            obs (list): List of observations from each environment after stepping.
            rewards (list): List of rewards from each environment.
            terminateds (list): List of termination flags from each environment.
            truncateds (list): List of truncation flags from each environment.
            infos (list): List of info dictionaries from each environment.
        """

        assert self.envs is not None, "The environments must be initialized before stepping. Call reset() first."
        assert len(
            actions) == self.n_envs, "The number of actions must match the number of environments."

        obs = []
        rewards = []
        terminateds = []
        truncateds = []
        infos = []

        for env, action in zip(self.envs, actions):
            env.step(action)
            o, r, term, trunc, info = env.step(action)
            
            info['env_id'] = env.spec.id if env.spec else 'unknown'
            
            obs.append(o)
            rewards.append(r)
            terminateds.append(term)
            truncateds.append(trunc)
            infos.append(info)

        return obs, rewards, terminateds, truncateds, infos

    def render():
        raise NotImplementedError("Render method is not implemented.")

    def close(self):
        pass

    def _init_envs(self):
        """
        Initializes multiple Sinergym environments.
        Returns:
            list: List of initialized Sinergym environments.
        """
        envs = [gym.make(env_id) for env_id in self.env_ids]
        [info(f'Env {env_id} has been created.') for env_id in self.env_ids]
        return envs
