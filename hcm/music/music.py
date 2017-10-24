import numpy as np

from scipy.interpolate import interp1d


def scale_constructor(f0, key, num_octaves):
    """Makes a vector of frequencies to go over """
    init_octave = np.zeros(len(key))
    for n in range(0, len(init_octave)):
        init_octave[n] = f0 * 2 ** (key[n] / 12.)
    all_octaves = np.zeros([num_octaves, len(key)])
    for i in range(0, num_octaves):
        all_octaves[i] = 2 ** i * init_octave
    return np.concatenate(all_octaves)


def frequency_map(signal, scale):
    """Maps control voltage to position on scale.

    Takes a control voltage (CV) signal, whose range is on [-1.0, 1.0] and maps
    it to a corresponding position on the scale.
    Returns an array of
    """
    interp = interp1d([-1, 1], [0, len(scale) - 1])
    f = np.zeros(len(signal))
    for n in range(0, len(signal)):
        index = int(interp(signal[n]))
        f[n] = scale[index]
    return f


def tempo_to_frequency(tempo, note_duration):
    """Given tempo (in BPM) and note duration, gives corresponding frequency.

    """
    # assign appropriate numerical factor to note type
    if note_duration == 'whole':
        note = -2.0
    if note_duration == 'half':
        note = -1.0
    if note_duration == 'quarter':
        note = 0.0
    if note_duration == 'eighth':
        note = 1.0
    if note_duration == 'sixteenth':
        note = 2.0

    # calculate frequency
    frequency = (tempo / 60.) * 2 ** note  # [Hz]
    return frequency
