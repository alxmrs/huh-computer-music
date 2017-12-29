import numpy as np
import scipy.io.wavfile as wavfile


def add_channels(signals):
    return np.array(np.vstack(signals)).T


def append(*signals):
    return np.array(np.hstack(signals))


def wav_read(filename):
    """Import .wav files from current directory. """
    return wavfile.read(filename)[1]


def wav_write(filename, sample_rate, file):
    """Export array to .wav file in current directory. """
    return wavfile.write(filename, sample_rate, file)