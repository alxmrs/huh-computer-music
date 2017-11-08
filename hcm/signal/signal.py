from hcm.io.channel import add_channels
import numpy as np


def time(t0, T, sample_rate, num_channels: int=1):
    """Just np.linspace()

    t = [t[0], t[1], t[2], ..., t[n], ..., t[N]].
    t[N] = t0 + N*dt = T
    dt = 1/sample_rate
    """
    ts = add_channels(
        [np.linspace(t0, t0 + T, num=T * sample_rate, dtype=np.float32)
         for _ in range(num_channels)]
    )

    return ts
