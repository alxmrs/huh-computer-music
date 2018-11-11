import numpy as np

import hcm

# allow voltage control of osc frequency
# here freq is now an array w/ same length as t


def VCO(t, f, osc):
    """Allows control of frequency in time.

    f is now a 1-D array with same length as t, so that the frequency can be
    specified at each point in time.
    Argument 'osc' can be sine, square, or triangle.
    """
    N = len(t)
    output = np.zeros(N, dtype=np.float32)
    for n in range(0, N):
        output[n] = osc(t[n], f[n])
    return output


def VCA(signal, modulation):
    """Amplitude modulation of two signals by pairwise multiplication. """
    return np.multiply(signal, modulation)


def ADSR(A, D, S, R, duration, sample_rate):
    """TODO: Find good place for this... """
    attack = (1.0 - 0.0) / A * hcm.ts.time(0, A, sample_rate)
    decay = 1 - S / D * hcm.ts.time(0, D, sample_rate)
    release = S - (S - 0.0) / R * hcm.ts.time(0, R, sample_rate)
    sustain = S * np.ones(int(duration * sample_rate) - len(attack) - len(decay) - len(release))

    return np.concatenate([attack, decay, sustain, release])

