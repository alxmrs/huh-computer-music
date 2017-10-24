import numpy as np


def add_channels(signals):
    return np.array(np.vstack(signals)).T
