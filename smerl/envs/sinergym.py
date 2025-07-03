import gymnasium as gym

import sinergym

from sinergym.utils.wrappers import (
    LoggerWrapper,
    NormalizeAction,
    NormalizeObservation,
    CSVLogger
)

from smerl.utils.aux import print_info


class SinergymMetaEnv(gym.Env):
    """
    Meta Sinergym environment.
    """

    def __init__(self, env_ids):
        """
        Class constructor for SinergymMetaEnv.
        Args:
            env_ids (list): List of Sinergym environment IDs to initialize.
        """

        self.env_ids = env_ids
        self.n_envs = len(env_ids)

        # Initialize multiple Sinergym environments
        self.envs = self._init_envs()

    def reset(self):
        """
        Resets all Sinergym environments and returns initial observations and infos.
        Returns:
            obs (list): List of initial observations from each environment.
            infos (list): List of info dictionaries from each environment.
        """

        # Reset all environments and collect initial observations
        obs, infos = [], []

        for env in self.envs:
            observation, info = env.reset()
            obs.append(observation)
            info['env_id'] = env.spec.id if env.spec else 'unknown'
            infos.append(info)

        return obs, infos

    def step(self, actions):
        """
        Steps through all Sinergym environments with the provided actions.
        Args:
            actions (list): List of actions for each environment.
        Returns:
            obs (list): List of observations from each environment after stepping.
            rewards (list): List of rewards from each environment.
            terminateds (list): List of termination flags from each environment.
            truncateds (list): List of truncation flags from each environment.
            infos (list): List of info dictionaries from each environment.
        """

        assert len(
            actions) == self.n_envs, "The number of actions must match the number of environments."

        obs = []
        rewards = []
        terminateds = []
        truncateds = []
        infos = []

        for env, action in zip(self.envs, actions):
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
        """
        Closes all the environments.
        """
        for env in self.envs:
            env.close()

    def _init_envs(self):
        """
        Initializes multiple Sinergym environments. Adds default normalization and logging wrappers to each environment.
        Returns:
            list: List of initialized Sinergym environments.
        """
        envs = [self._wrap_environment(gym.make(env_id))
                for env_id in self.env_ids]
        [print_info(f'Environment {env_id} has been created.')
         for env_id in self.env_ids]

        return envs

    def _wrap_environment(self, env):
        """
        Wraps a Sinergym environment with additional wrappers.
        Args:
            env: The Sinergym environment to wrap.
        Returns:
            Wrapped environment.
        """
        env = LoggerWrapper(env)
        env = NormalizeAction(env)
        env = NormalizeObservation(env)
        env = CSVLogger(env)

        return env
