import numpy as np

def time(t0, T, sample_rate):
    """
    Just np.linspace()
    t = [t[0], t[1], t[2], ..., t[n], ..., t[N]].
    t[N] = t0 + N*dt = T
    dt = 1/sample_rate
    """
    t = np.linspace(t0, t0+T, num=T*sample_rate)
    return t