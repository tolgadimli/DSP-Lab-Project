# DSP LAB Midterm Q1
# author: Tolga

import pyaudio, struct
import tkinter as Tk   	
import wave

import numpy as np
from sound_effects import *
from utils import *
from tkinter import scrolledtext

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time
import threading



def fun_quit():
    global CONTINUE
    CONTINUE = False

def fun_pause():
    global PAUSE
    PAUSE = True

def fun_resume():
    global PAUSE
    PAUSE = False

def case_noeffect():
    global CASE_EFFECT
    CASE_EFFECT = 0

def case_amplitude_mod():
    global CASE_EFFECT
    CASE_EFFECT = 1

def case_alien():
    global CASE_EFFECT
    CASE_EFFECT = 2

def case_darth_vader():
    global CASE_EFFECT
    CASE_EFFECT = 3

def case_baby():
    global CASE_EFFECT
    CASE_EFFECT = 4

def case_no_sound():
    global CASE_SOUND
    CASE_SOUND = 0

def case_harbour_sound():
    global CASE_SOUND
    CASE_SOUND = 1

def case_park_sound():
    global CASE_SOUND
    CASE_SOUND = 2

def case_starwars_sound():
    global CASE_SOUND
    CASE_SOUND = 3

def case_space_sound():
    global CASE_SOUND
    CASE_SOUND = 4

# Thread function
def get_speech2text(buffer, ls):
    res = stt.recognize(audio=buffer, content_type='audio/l16;rate=%d;endianness=little-endian'%RATE, model='en-US_BroadbandModel').get_result() #en-US_Multimedia en-US_Telephony US_BroadbandModel
    #res = stt.recognize(audio=buffer, content_type='audio/l16;rate=%d'%RATE, model='en-US_BroadbandModel').get_result()
    if len(res) > 0:
        if len(res['results'])> 0:
            text = res['results'][0]['alternatives'][0]['transcript']
            
            #print(res)
            ls.append(text)

################################ MAIN PROGRAM

# Connection to speech to text module
apikey = 'pss_w5M126orHdw5aCBL2Z8FK8YEDtdCM8KEyMOnqm98'
url = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/07ae78a0-1395-4360-905c-fbb909d007e8'
head = {'Transfer-Encoding': 'chunked'}

authenticator = IAMAuthenticator(apikey ) #,headers=head)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)
#stt.set_disable_ssl_verification(True) # ?????


# Read wave file properties
RATE        = 44100     # Frame rate (frames/second)
WIDTH       = 2     # Number of bytes per sample
CHANNELS    = 1     # Number of channels
BLOCKLEN    = 1024
PAUSE       = False
CONTINUE    = True
CASE_EFFECT = 0
CASE_SOUND = 0

wave_harbor, harbor_len, harbor_width = get_harbour_wave()
wave_park, park_len, park_width = get_park_wave()
wave_space, space_len, space_width = get_space_wave()
wave_starwars, starwars_len, starwars_width = get_starwars_wave()


# Define Tkinter root
root = Tk.Tk()
root.geometry('1400x500')

Label_effect = Tk.Label(root, text='Sound Effects', font=("Georgia, 16"))
B_none = Tk.Button(root, text = 'No Effect', command = case_noeffect, height = 5, width = 12, image = "no_effect.png", compound=TOP)
B_amp = Tk.Button(root, text = 'Robot', command = case_amplitude_mod, height = 5, width = 12, image = "robot.png", compound=TOP)
B_dv = Tk.Button(root, text = 'Darth Vader', command = case_darth_vader, height = 5, width = 12, image = "dv.png", compound=TOP)
B_al = Tk.Button(root, text = 'Alien', command = case_alien, height = 5, width = 12, image = "alien.png", compound=TOP)
B_bb = Tk.Button(root, text = 'Baby', command = case_baby, height = 5, width = 12, image = "baby.png", compound=TOP)


Label_sound = Tk.Label(root, text='Background Sounds', font=("Georgia, 16"))
B_harbor = Tk.Button(root, text = 'Harbor', command = case_harbour_sound, height = 5, width = 12, image = "sea.png", compound=TOP)
B_park = Tk.Button(root, text = 'Park', command = case_park_sound, height = 5, width = 12, image = "park.png", compound=TOP)
B_sw = Tk.Button(root, text = 'Star Wars', command = case_starwars_sound, height = 5, width = 12, image = "star_wars.png", compound=TOP)
B_space = Tk.Button(root, text = 'Outer Space', command = case_space_sound, height = 5, width = 12, image = "space.png", compound=TOP)
B_none_sound = Tk.Button(root, text = 'No Sound', command = case_no_sound, height = 5, width = 12, image = "no_effect.png", compound=TOP)

B_resume = Tk.Button(root, text = 'Resume', command = fun_resume, height = 5, width = 12, image = "play.png", compound=TOP)
B_pause = Tk.Button(root, text = 'Pause', command = fun_pause, height = 5, width = 12, image = "pause.png", compound=TOP)
B_quit = Tk.Button(root, text = 'Save & Quit', command = fun_quit, height = 5, width = 12)

text=Tk.scrolledtext.ScrolledText(root, font=("Georgia, 16"))
# for i in range(150):
#     text.configure(state='normal')
#     text.insert(Tk.END, "Deneme Deneme Deneme...\n")
#     text.see(Tk.END)
    #text.configure(state='disabled')

# Place widgets
B_amp.grid(row=0,column=0)
B_dv.grid(row=1,column=0)
B_al.grid(row=2,column=0)
B_bb.grid(row=3,column=0)
B_none.grid(row=4,column=0)

B_harbor.grid(row=0,column=1)
B_park.grid(row=1,column=1)
B_sw.grid(row=2,column=1)
B_space.grid(row=3,column=1)
B_none_sound.grid(row=4,column=1)

B_resume.grid(row=0,column=8)
B_pause.grid(row=1,column=8)
B_quit.grid(row=3,column=8)

text.grid(row=0, rowspan=6, column=2, columnspan=6)
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

output_wavfile = 'recording.wav'
output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Buffer to store past signal values. Initialize to zero.
n = 0
transcript = []
buffer = b''
flag = 0
OVERLAP_AMOUNT = 5 # number of overlapping blocks for speech to text

while CONTINUE:
    if not PAUSE:
        start_index = n*BLOCKLEN
        if n % 10 == 0: #updating the root every 50 samples since it slows down the program
            #a = time.time()
            root.update()
            #print(time.time() - a)


        # Speech to text transcription part
        input_bytes = stream_in.read(BLOCKLEN, exception_on_overflow = False)
        buffer += input_bytes
        if flag > 100:
            
            T = threading.Thread(target=get_speech2text, args=(buffer, transcript))
            T.setDaemon(True) 
            T.start()
            flag = 0
            buffer = buffer[len(buffer)-OVERLAP_AMOUNT*BLOCKLEN:len(buffer)]
            #buffer = b''
            if len(transcript) > 0:
                text.delete(1.0,Tk.END)
                transcripted_text = "".join(transcript)
                transcripted_text = transcripted_text.replace("%HESITATION", "uhm")
                text.insert(Tk.END, transcripted_text)
            root.update()
                #print("".join(transcript))
            #transcript = []

        flag = flag + 1

        input_block = struct.unpack('h' * BLOCKLEN, input_bytes)  # Convert

        if CASE_EFFECT == 0:
            output_block = input_block
            #print("DEFAULT")

        elif CASE_EFFECT == 1:    # Amplitude Mod
            output_block = amplitude_mod(RATE, start_index, input_block, fc = 100, A = 2, phase = 0 )
            output_block = np.round(output_block).astype(int)
            #print("AMP MOD")
            
        elif CASE_EFFECT == 2:     # Alien
            output_block = pitch_shifter(RATE, start_index, input_block, shift = 5)
            output_block = np.round(output_block).astype(int)
            #print("Alien")

        elif CASE_EFFECT == 3:     # Darth Vader
            output_block = darth_vader(RATE, start_index, input_block, speed_factor=0.8, delay=0.02, low_freq=200)
            output_block = np.round(output_block).astype(int)
            #print("Darth Vader") 

        elif CASE_EFFECT == 4:     # Baby
            output_block = pitch_shifter(RATE, start_index, input_block, shift = 20)
            output_block = baby(RATE, start_index, output_block, speed_factor=2.0, freq=0.4)
            output_block = np.round(output_block).astype(int)
            #print("Baby") 


        if CASE_SOUND == 0:
            output_block_snd = output_block
        elif CASE_SOUND == 1:
            output_block_snd = add_sound(output_block, n, wave_harbor, harbor_len, harbor_width)
        elif CASE_SOUND == 2:
            output_block_snd = add_sound(output_block, n, wave_park, park_len, park_width)
        elif CASE_SOUND == 3:
            output_block_snd = add_sound(output_block, n, wave_starwars, starwars_len, starwars_width)
        elif CASE_SOUND == 4:
            output_block_snd = add_sound(output_block, n, wave_space, space_len, space_width)

        binary_data = struct.pack('h' * BLOCKLEN, *output_block_snd)
        output_wf.writeframes(binary_data)
        #stream_out.write(binary_data)
        n = n + 1
    else: 
        root.update()

print('* Finished')

stream_in.stop_stream()
stream_out.stop_stream()

stream_in.close()
stream_out.close()
print('Saving the audio and the transcripted text.')
output_wf.close()
print("Quitting.")
p.terminate()
