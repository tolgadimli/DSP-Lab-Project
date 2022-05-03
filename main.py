# DSP LAB Midterm Q1
# author: Tolga

import pyaudio, struct
import tkinter as Tk   	
import wave

import numpy as np
from sound_effects import *
from utils import *


def fun_quit():
    global CONTINUE
    print('Good bye')
    CONTINUE = False

def case_amplitude_mod():
    global CASE
    CASE = 1



################################ MAIN PROGRAM

# Read wave file properties
RATE        = 44100     # Frame rate (frames/second)
WIDTH       = 2     # Number of bytes per sample
CHANNELS    = 1     # Number of channels
BLOCKLEN    = 1024
CONTINUE    = True
CASE = 0

# Define Tkinter root
root = Tk.Tk()

B_amp = Tk.Button(root, text = 'Amplitude Modulation', command = case_amplitude_mod)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets
B_amp.pack(side = Tk.BOTTOM, fill = Tk.X)
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)

# Open an output audio stream
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream_in = p.open(
    format = PA_FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = 256)

# Open the output stream
stream_out = p.open(
    format = PA_FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = False,
    output = True,
    frames_per_buffer = 256)         
  # specify low frames_per_buffer to reduce latency

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN =  2*1024         # Set buffer length.
buffer = BUFFER_LEN * [0]   # list of zeros
print('The buffer is %d samples long.' % BUFFER_LEN)
n = 0
while CONTINUE:
    
    start_index = n*BLOCKLEN
    if n % 20 == 0: #updating the root every 50 samples since it slows down the program
        root.update()

    input_bytes = stream_in.read(BLOCKLEN)
    input_block = struct.unpack('h' * BLOCKLEN, input_bytes)  # Convert


    if CASE == 0:
        output_block = input_block
        #print("DEFAULT")

    elif CASE == 1:
        output_block = amplitude_mod(RATE, start_index, input_block, fc = 1000, A = 2, phase = 0 )
        output_block = np.round(output_block).astype(int)
        #print("AMP MOD")
        
    elif CASE == 2:     # Alien
        output_block = pitch_shifter(RATE, input_block, fr = 20, shift = 5)
        output_block = np.round(output_block).astype(int)
        #print("Alien MOD")  

    binary_data = struct.pack('h' * BLOCKLEN, *output_block)
    stream_out.write(binary_data)
    n = n + 1

print('* Finished')

stream_in.stop_stream()
stream_out.stop_stream()

stream_in.close()
stream_out.close()

p.terminate()
