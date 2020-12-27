import numpy as np

def sine_wave(t, f, phi=0, A=1):
    """
    Sine wave: frequency, amplitude, and phase-adjustable oscillator.

    Parameters
    ----------
    t : 1-D array
        Time.
    f : scalar or 1-D array
        Frequency.
    A : scalar or 1-D array
        Amplitude, defaults to 1.
    phi : scalar or 1-D array
        Phase, defaults to 0.

    Returns
    ----------
    out : 1-D array
        Time series array of sine wave.
    """
    x = np.multiply(A, np.sin(np.add(np.multiply(2*np.pi*f, t), phi)))
    return x


def square_wave(t, f, d=.5, phi=0, A=1):
    """
    Square wave: frequency, duty cycle, amplitude, and phase-adjustable oscillator.

    Parameters
    ----------
    t : 1-D array
        Time.
    f : scalar or 1-D array
        Frequency.
    d : scalar or 1-D array
        Duty cycle. Values must fall within [0,1].
        Set d=0.5 for square wave.
    A : scalar or 1-D array
        Amplitude, defaults to 1.
    phi : scalar or 1-D array
        Phase, defaults to 0.

    Returns
    ----------
    out : 1-D array
        Time series array of square or pulse wave.

    """
    x = np.multiply(A, signal.square(np.add(np.multiply(2*np.pi*f, t), phi), d))
    return x


def sawtooth_wave(t, f, d=0, phi=0, A=1):
    """
    Sawtooth wave: frequency, duty cycle, amplitude, and phase-adjustable oscillator.

    Parameters
    ----------
    t : 1-D array
        Time.
    f : scalar or 1-D array
        Frequency.
    d : scalar or 1-D array
        Duty cycle. Values must fall within [0,1].
        Set d=0.5 for triangle wave. d=0 for negative slope sawtooth, d=1 for positive slope sawtooth.
    A : scalar or 1-D array
        Amplitude, defaults to 1.
    phi : scalar or 1-D array
        Phase, defaults to 0.

    Returns
    ----------
    out : 1-D array
        Time series array of triangle or sawtooth wave.

    """
    x = np.multiply(A, signal.sawtooth(np.add(np.multiply(2*np.pi*f, t), phi), d))
    return x
