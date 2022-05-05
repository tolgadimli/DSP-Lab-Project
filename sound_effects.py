from math import sin, cos, pi
import numpy as np
import scipy.signal as signal
from scipy.signal import hilbert

def amplitude_mod(RATE, index, x, fc = 2000, A = 5000, phase = 0 ):

    x_arr = np.asarray(x)
    carrier_signal = [ A*sin(2*pi*fc*n/RATE + phase) for n in range(index, index+1024)]
    carrier_signal = np.asarray(carrier_signal)
    y = (1+x_arr)*carrier_signal
    return y


def pitch_shifter(RATE, index, x, shift = 5):
    sz = 2*1024   # Read and process 1/fr second at a time.
    x_arr = np.asarray(x)
    lf = np.fft.rfft(x_arr, 1024) 
    lf = np.roll(lf, shift)
    lf[0:shift] = 0
    nl = np.fft.irfft(lf)
    ns = np.column_stack((nl)).ravel().astype(np.int16)

    return ns    
        
    
def darth_vader(RATE, index, x, speed_factor, delay, low_freq):
    # speed
    x_arr = np.asarray(x)
    num = len(x_arr)
    sound_index = np.round(np.arange(0, 1024, speed_factor)).astype(int)
    slow_x = x_arr[sound_index[:1024]]
    
    # echo
    echo_x = slow_x
    output_delay = delay * RATE

    for count, e in enumerate(slow_x):
        echo_x[count] = e + slow_x[count - int(output_delay)]
        
        
    # lowpass
    nyquist = RATE / 2.0
    cutoff = low_freq / nyquist
    x, y = signal.butter(4, 0.4, btype='lowpass', analog=False)
    low_x = signal.filtfilt(x, y, echo_x)

    return low_x


def baby(RATE, start_index, x, speed_factor=2.0, freq=200):
    # speed
    x_arr = np.asarray(x)
    num = len(x_arr)
    sound_index = np.round(np.arange(0, num, speed_factor)).astype(int)
    slow_x = x_arr[sound_index[:1024//2]]
    slow_x = np.repeat(slow_x,2)

    x, y = signal.butter(4, 0.5, btype='lowpass', analog=False)
    low_x = signal.filtfilt(x, y, slow_x)

    return low_x
    
# def robotic(RATE, index, m, fc = 2000):
#     mh = hilbert(m)
#     carrier_signal = [ A*sin(2*pi*fc*n/RATE) for n in range(index, index+1024)]

#     sbu = 2 * m *  
