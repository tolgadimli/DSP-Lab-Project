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
        
    
def darth_vader(RATE, x, speed_factor, delay, low_freq):
    # speed
    num = len(x)
    sound_index = np.round(np.arange(0, num, speed_factor))
	slow_x = x[sound_index[sound_index < num].astype(int)]
    
    # echo
    echo_x = np.zeros(num)
    output_delay = delay * RATE

    for count, e in enumerate(slow_x):
        echo_x[count] = e + slow_x[count - int(output_delay)]
        
        
    # lowpass
    nyquist = RATE / 2.0
    cutoff = low_freq / nyquist
    x, y = signal.butter(order=4, cutoff, btype='lowpass', analog=False)
    low_x = signal.filtfilt(x, y, echo_x)
    
    return low_x
    
# def robotic(RATE, index, m, fc = 2000):
#     mh = hilbert(m)
#     carrier_signal = [ A*sin(2*pi*fc*n/RATE) for n in range(index, index+1024)]

#     sbu = 2 * m *  
