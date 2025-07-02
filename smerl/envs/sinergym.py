import gymnasium as gym
import numpy as np

import sinergym

class SinergymMetaEnv(gym.Env):
    """
    Meta Sinergym environment.
    """
    
    def __init__(self, n_envs=1):
        """
        Class constructor for SinergymMetaEnv.
        """
        
        self.n_envs = n_envs

        self.envs = self._init_envs()

    def reset(self):
        return None, None

    def step(self, action):
        pass

    def render():
        raise NotImplementedError("Render method is not implemented.")
    
    def close(self):
        pass

    def _init_envs(self):
        """
        Initializes multiple Sinergym environments.

        Returns:
            list: A list of initialized Sinergym environments.
        """
        
        envs = []

        for i in range(self.n_envs):
            env = gym.make('Eplus-5zone-mixed-continuous-stochastic-v1')
            envs.append(env)
            print(f'Env {i} has been created!')

        return envs