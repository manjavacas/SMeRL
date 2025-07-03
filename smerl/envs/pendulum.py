import gymnasium as gym

from smerl.utils.aux import print_info


class PendulumMetaEnv(gym.Env):
    """
    Meta Pendulum environment.
    """

    def __init__(self, gravities):
        """
        Class constructor for PendulumMetaEnv.
        Args:
            gravities (list): List of gravitational constants for each environment.
        """

        self.n_envs = len(gravities)
        self.gravities = gravities

        # Initialize multiple environments
        self.envs = self._init_envs()

    def reset(self):
        """
        Resets all environments and returns initial observations and infos.
        Returns:
            obs (list): List of initial observations from each environment.
            infos (list): List of info dictionaries from each environment.
        """

        # Reset all environments and collect initial observations
        obs, infos = [], []

        for i, env in enumerate(self.envs):
            observation, info = env.reset()
            obs.append(observation)
            info['gravity'] = self.gravities[i]
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

        for i, (env, action) in enumerate(zip(self.envs, actions)):
            o, r, term, trunc, info = env.step(action)
            info['gravity'] = self.gravities[i]

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
        Initializes multiple environments with specified gravitational constants.
        Returns:
            list: List of initialized environments.
        """
        envs = []
        for gravity in self.gravities:
            envs.append(gym.make('Pendulum-v1', g=gravity))
            print_info(f'Pendulum environment with gravity {gravity} has been created.')

        return envs
