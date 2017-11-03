import numpy as np


def normalize(signal):
    """Restrict the range of a signal to the closed interval [-1.0, 1.0]. """
    normalized_signal = signal / max(signal.max(), signal.min(), key=abs)
    return normalized_signal


def AM(signal, modulation):
    """Amplitude modulation of two signals by pairwise multiplication. """
    return np.multiply(signal, modulation)


# hold = downsampled rate, or the number of times per second you want to sample
def sample_and_hold(signal, sample_rate, hold):
    """Samples"""
    inc = int(sample_rate / hold)
    samples = signal[0::inc]
    new_signal = np.zeros([len(samples), inc], dtype=np.float32)
    for i in range(0, len(samples)):
        new_signal[i, :] = samples[i]
    return np.concatenate(new_signal)
