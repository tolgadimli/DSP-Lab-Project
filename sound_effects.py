from math import sin, cos, pi
import numpy as np
from scipy.signal import hilbert

def amplitude_mod(RATE, index, x, fc = 2000, A = 5000, phase = 0 ):

    x_arr = np.asarray(x)
    carrier_signal = [ A*sin(2*pi*fc*n/RATE + phase) for n in range(index, index+1024)]
    carrier_signal = np.asarray(carrier_signal)
    y = (1+x_arr)*carrier_signal
    return y

# def robotic(RATE, index, m, fc = 2000):
#     mh = hilbert(m)
#     carrier_signal = [ A*sin(2*pi*fc*n/RATE) for n in range(index, index+1024)]

#     sbu = 2 * m *  