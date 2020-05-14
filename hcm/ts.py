import numpy as np


def normalize(signal):
    """Restrict the range of a signal to the closed interval [-1.0, 1.0]. """
    normalized_signal = signal / max(signal.max(), signal.min(), key=abs)
    return normalized_signal


# hold = downsampled rate, or the number of times per second you want to sample
def sample_and_hold(signal, sample_rate, hold):
    """Samples"""
    inc = int(sample_rate / hold)
    samples = signal[0::inc]
    new_signal = np.zeros([len(samples), inc], dtype=np.float32)
    for i in range(0, len(samples)):
        new_signal[i, :] = samples[i]
    return np.concatenate(new_signal)


def time(t0, T, sample_rate):
    """Just np.linspace()

    t = [t[0], t[1], t[2], ..., t[n], ..., t[N]].
    t[N] = t0 + N*dt = T
    dt = 1/sample_rate
    """
    t = np.linspace(t0, t0 + T, num=T * sample_rate, dtype=np.float32)
    return t
