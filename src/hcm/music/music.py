import numpy as np

from hcm.music.const import DURATIONS


def scale_constructor(f0, key, num_octaves):
    """Makes a vector of frequencies to go over """
    init_octave = np.zeros(len(key))
    for n in range(0, len(init_octave)):
        init_octave[n] = f0 * 2 ** (key[n] / 12.)
    all_octaves = np.zeros([num_octaves, len(key)])
    for i in range(0, num_octaves):
        all_octaves[i] = 2 ** i * init_octave
    return np.concatenate(all_octaves)


def frequency_map(signal: np.ndarray, scale: np.ndarray) -> np.ndarray:
    """Maps control voltage to position on scale.

    Takes a control voltage (CV) signal, whose range is on [-1.0, 1.0] and maps
    it to a corresponding position on the scale.
    Returns an array of

    :param signal:
    :param scale:
    :return:

    >>> signal = np.array([-1., -.5, .0, .5, 1.])
    >>> frequency_map(signal, np.array([100, 200, 300, 400, 500]))
    array([ 100.,  200.,  300.,  400.,  500.])
    >>> frequency_map(signal, np.array([100, 200]))
    array([ 100.,  100.,  100.,  100.,  200.])
    >>> frequency_map(signal, np.array([100, 200, 300]))
    array([ 100.,  100.,  200.,  200.,  300.])
    >>> frequency_map(signal, np.array([100]))
    array([ 100.,  100.,  100.,  100.,  100.])
    >>> frequency_map(signal, \
            np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]))
    array([  100.,   300.,   500.,   700.,  1000.])
    >>> frequency_map(signal, np.array([100, 200, 300, 400, 500, 600, 700]))
    array([ 100.,  200.,  400.,  500.,  700.])
    """

    bins = np.linspace(-1, 1, num=len(scale))
    inds = np.digitize(signal, bins)
    f = np.array([scale[i - 1] for i in inds], dtype=np.float32)

    return f


def tempo_to_frequency(tempo, note_duration='quarter'):
    """Given tempo (in BPM) and note duration, gives corresponding frequency.

    """

    # assign appropriate numerical factor to note type
    if note_duration not in DURATIONS:
        raise UserWarning('{} not a valid note duration, defaulting to quarter notes.')

    note = DURATIONS.get(note_duration, 0)

    # calculate frequency
    frequency = (tempo / 60.) * 2 ** note  # [Hz]
    return frequency


if __name__ == '__main__':
    import doctest

    doctest.testmod()
