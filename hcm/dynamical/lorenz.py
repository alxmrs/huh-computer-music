from hcm.ts import normalize
import numpy as np


def lorenz(t, time_scale):
    """Lorenz system

    Parameters s, r, b are fixed.
    Initial conditions also fixed, but with slight random perturbation to keep
    it interesting.
    """
    # params
    s = 10
    r = 28
    b = 8 / 3.
    # initialize state vector
    X0 = [2, 3, 4]
    X = np.zeros([len(X0), len(t)])
    # label state variables
    x = X[0]
    y = X[1]
    z = X[2]
    # assign initial condition
    X[:, 0] = X0
    # define time step
    dt = (t[1] - t[0]) * time_scale
    # equations of motion
    for n in range(0, len(t) - 1):
        x[n + 1] = x[n] + dt * (s * (y[n] - x[n]))
        y[n + 1] = y[n] + dt * (r * x[n] - y[n] - x[n] * z[n])
        z[n + 1] = z[n] + dt * (x[n] * y[n] - b * z[n])
    # normalize
    x = normalize(x)
    y = normalize(y)
    z = normalize(z)
    return x, y, z
