from gymnasium.envs.registration import register

register(
    id='meta-pendulum-v0',
    entry_point='smerl.envs.pendulum:PendulumMetaEnv'
)

register(
    id='meta-pendulum-sampled-v0',
    entry_point='smerl.envs.pendulum:PendulumSampledMetaEnv'
)


register(
    id='meta-sinergym-v0',
    entry_point='smerl.envs.sinergym:SinergymMetaEnv'
)

