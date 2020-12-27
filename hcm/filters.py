# FILTERS: lowpass, highpass, bandpass...

# what are acceptable values for fc, k?
# need a wrapper to take values in range [0,1]?
def lowpass(x, fc, k, sample_rate=R):
    # state variables
    y1 = np.zeros(len(x))
    y2 = np.zeros(len(y1))
    y3 = np.zeros(len(y2))
    y4 = np.zeros(len(y3))
    # define angular frequency
    omega = np.multiply(2*np.pi, fc)
    # initial conditions
    y1[0] = omega[0]/(1+omega[0]) * x[0]
    y2[0] = omega[0]/(1+omega[0]) * y1[0]
    y3[0] = omega[0]/(1+omega[0]) * y2[0]
    y4[0] = omega[0]/(1+omega[0]) * y3[0]
    dt = 1/sample_rate
    for n in range(len(x)-1):
        y1[n+1] = y1[n] + dt * omega[n] * (x[n] - y1[n] - k[n] * y4[n])
        y2[n+1] = y2[n] + dt * omega[n] * (y1[n] - y2[n])
        y3[n+1] = y3[n] + dt * omega[n] * (y2[n] - y3[n])
        y4[n+1] = y4[n] + dt * omega[n] * (y3[n] - y4[n])
    return y4

# what are acceptable values for fc, k?
# need a wrapper to take values in range [0,1]?
def highpass(x, fc, k, sample_rate=R):
    # state variables
    y1 = np.zeros(len(x))
    y2 = np.zeros(len(y1))
    y3 = np.zeros(len(y2))
    y4 = np.zeros(len(y3))
    # initial conditions
    y1[0] = x[0]
    y2[0] = y1[0]
    y3[0] = y2[0]
    y4[0] = y3[0]
    dt=1/sample_rate
    alpha = 1/(2*np.pi*dt*fc+1)
    for n in range(len(x)-1):
        y1[n+1] = alpha[n] * (y1[n] + x[n+1] - x[n] - k[n] * y4[n])
        y2[n+1] = alpha[n] * (y2[n] + y1[n+1] - y1[n])
        y3[n+1] = alpha[n] * (y3[n] + y2[n+1] - y2[n])
        y4[n+1] = alpha[n] * (y4[n] + y3[n+1] - y3[n])
    return y4
