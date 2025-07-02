from gymnasium.envs.registration import register

register(
    id='sinergym-v0',
    entry_point='smerl.envs.sinergym:SinergymMetaEnv'
)