from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pyaudio
import struct
import time
import threading



# Thread function
def get_speech2text(buffer, ls):
    res = stt.recognize(audio=buffer, content_type='audio/l16;rate=%d;endianness=little-endian'%RATE, model='en-US_Telephony').get_result() #en-US_Multimedia en-US_Telephony US_BroadbandModel
    #res = stt.recognize(audio=buffer, content_type='audio/l16;rate=%d'%RATE, model='en-US_BroadbandModel').get_result()
    if len(res) > 0:
        if len(res['results'])> 0:
            text = res['results'][0]['alternatives'][0]['transcript']
            print(res)
            ls.append(text)



apikey = 'pss_w5M126orHdw5aCBL2Z8FK8YEDtdCM8KEyMOnqm98'
url = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/07ae78a0-1395-4360-905c-fbb909d007e8'


head = {'Transfer-Encoding': 'chunked'}

authenticator = IAMAuthenticator(apikey ) #,headers=head)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

# Read wave file properties
RATE        = 44100     # Frame rate (frames/second)
WIDTH       = 2     # Number of bytes per sample
CHANNELS    = 1     # Number of channels
BLOCKLEN    = 1024
CONTINUE    = True
CASE = 0

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
#buffer 

#res = stt.recognize(audio=input_bytes, content_type='audio/', model='en-US_BroadbandModel').get_result()
        
transcript = []
buffer = b''
flag = 0
OVERLAP_AMOUNT = 5 # number of overlapping blocks for speech to text

while CONTINUE:

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
            print("".join(transcript))
        #transcript = []


    #print(len(buffer))
    flag = flag + 1
    input_block = struct.unpack('h' * BLOCKLEN, input_bytes)  # Convert
    output_block = input_block
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)
    #stream_out.write(binary_data)

print('* Finished')

stream_in.stop_stream()
stream_out.stop_stream()

stream_in.close()
stream_out.close()

p.terminate()
