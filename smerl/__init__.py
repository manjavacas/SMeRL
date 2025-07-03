from gymnasium.envs.registration import register

register(
    id='meta-pendulum-v0',
    entry_point='smerl.envs.pendulum:PendulumMetaEnv'
)

register(
    id='meta-sinergym-v0',
    entry_point='smerl.envs.sinergym:SinergymMetaEnv'
)

