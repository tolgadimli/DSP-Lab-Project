from math import sin, cos, pi
import numpy as np
import scipy.signal as signal
from scipy.signal import hilbert
import struct

def amplitude_mod(fs, index, x, fc = 2000, A = 5000, phase = 0 ):

    length = len(x)
    x_arr = np.asarray(x)
    carrier_signal = [ A*sin(2*pi*fc*n/fs + phase) for n in range(index, index+length)]
    carrier_signal = np.asarray(carrier_signal)
    y = (1+x_arr)*carrier_signal

    a, b = signal.butter(4, 0.5, btype='lowpass', analog=False)
    y_low = signal.filtfilt(a, b, y)

    return y_low

def robotic(fs, index, m, fc = 2000):

    length = len(m)
    m_arr = np.asarray(m)

    mh = hilbert(m)
    # print(length)
    # print(type(mh))
    

    carrier_signal_sin = np.array([ sin(2*pi*fc*n/fs) for n in range(index, index+length)])
    carrier_signal_cos = np.array([ cos(2*pi*fc*n/fs) for n in range(index, index+length)])

    sbu = 2 * m_arr *  carrier_signal_cos - np.real(mh * 2 * carrier_signal_sin)
    sbl = 2 * m_arr *  carrier_signal_cos + np.real(mh * 2 * carrier_signal_sin)

    y = sbu + m_arr + sbl
    a, b = signal.butter(4, 0.5, btype='lowpass', analog=False)
    y_low = signal.filtfilt(a, b, y)

    return y_low

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
    

def add_sound(x, block_ind, wf, wave_length, wave_width):
    #x_arr = np.asarray(x)
    L = len(x)
    if (block_ind + 1) * L < wave_length:
        wf.setpos(block_ind * L)
    else:
        wf.setpos(0) 
        
    sound_portion_bin = wf.readframes(L)
    sound_portion = struct.unpack('h' * L, sound_portion_bin) 
    sound_portion_arr = np.asarray(sound_portion)
    y = x + sound_portion_arr

    return y
