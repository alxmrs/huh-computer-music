import numpy as np


def comparator(x, threshold):
    out = np.zeros(len(x))
    out[np.nonzero(x > threshold)] = 1.0
    return out


def trigger(x, threshold):
    trig = np.zeros(len(x))
    trig[np.nonzero(x > threshold)] = 1.0

    for n in range(1, len(x)):
        window = [x[n - 1], x[n]]

        if window == [0.0, 1.0]:
            trig[n] = 1.0
        if window == [1.0, 0.0]:
            trig[n] = 1.0

    return trig


def sampler(sample, trig):
    out = np.zeros(len(trig))
    indices = np.nonzero(trig == 1)[0]

    for i in range(len(indices)):
        ind = indices[i]
        end = min(ind + len(sample), len(trig))
        diff = end - ind
        out[ind:end] = sample[:diff]

    return out[:len(trig)]
