import numpy as np

from hcm.ts import normalize


def lorenz(t, X0=(2, 3, 4), time_scale=1):
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
    X = np.zeros([len(X0), len(t)])
    # label state variables
    x, y, z = X[0:3]
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
    x, y, z = map(normalize, (x, y, z))
    return x, y, z


def dlorenz(t, x, y, z):
    # params
    s = 10
    r = 28
    b = 8 / 3.
    dx = np.zeros(len(x))
    dy = np.zeros(len(y))
    dz = np.zeros(len(z))
    for n in range(len(t) - 1):
        dx[n + 1] = s * (y[n] - x[n])
        dy[n + 1] = r * x[n] - y[n] - x[n] * z[n]
        dz[n + 1] = x[n] * y[n] - b * z[n]
    # normalize
    dx, dy, dz = map(normalize, (dx, dy, dz))
    return dx, dy, dz
