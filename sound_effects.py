from math import sin, cos, pi
import numpy as np
from scipy.signal import hilbert

def amplitude_mod(RATE, index, x, fc = 2000, A = 5000, phase = 0 ):

    x_arr = np.asarray(x)
    carrier_signal = [ A*sin(2*pi*fc*n/RATE + phase) for n in range(index, index+1024)]
    carrier_signal = np.asarray(carrier_signal)
    y = (1+x_arr)*carrier_signal
    return y


def pitch_shifter(RATE, x, fr = 20, shift = 5):
    fr = 20         # A larger number for fr means less reverb.
    sz = RATE//fr   # Read and process 1/fr second at a time.
    shift = 100//fr # shifting 100 Hz
    x_arr = np.asarray(x)
     
    lf = np.fft.rfft(x, 100)
    lf = np.roll(lf, shift)
    lf[0:shift] = 0
    nl = np.fft.irfft(lf)
    ns = np.column_stack((nl)).ravel().astype(np.int16)

    return ns    
        

# def robotic(RATE, index, m, fc = 2000):
#     mh = hilbert(m)
#     carrier_signal = [ A*sin(2*pi*fc*n/RATE) for n in range(index, index+1024)]

#     sbu = 2 * m *  
