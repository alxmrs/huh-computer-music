
import numpy as np

# allow voltage control of osc frequency
# here freq is now an array w/ same length as t
def VCO(t, f, osc):
    """
    Allows control of frequency in time.
    f is now a 1-D array with same length as t, so that the frequency can be
    specified at each point in time.
    Argument 'osc' can be sine, square, or triangle.
    """
    N = len(t);
    output = np.zeros(N);
    for n in range(0, N):
        output[n] = osc(t[n], f[n])
    return output
