import numpy as np


def sine(t, f):
    """Sine wave with frequency f, amplitude 1. """
    return np.sin(2 * np.pi * f * t)


def square(t, f):
    """Square wave with frequency f, amplitude 1. """
    return np.sign(np.sin(2 * np.pi * f * t))


def triangle(t, f):
    """Triangle wave with frequency f, amplitude 1. """
    return (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * f * t))
