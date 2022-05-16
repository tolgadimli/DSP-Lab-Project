import wave

def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return(x)


def get_harbour_wave():
    wavfile = 'waves/sea.wav'
    wf = wave.open( wavfile, 'rb' )
    signal_length   = wf.getnframes()       # Signal length
    width           = wf.getsampwidth()     # Sample width

    return wf, signal_length, width

def get_park_wave():
    wavfile = 'waves/park.wav'
    wf = wave.open( wavfile, 'rb' )
    signal_length   = wf.getnframes()       # Signal length
    width           = wf.getsampwidth()     # Sample width

    return wf, signal_length, width

def get_starwars_wave():
    wavfile = 'waves/star_wars.wav'
    wf = wave.open( wavfile, 'rb' )
    signal_length   = wf.getnframes()       # Signal length
    width           = wf.getsampwidth()     # Sample width

    return wf, signal_length, width

def get_space_wave():
    wavfile = 'waves/space.wav'
    wf = wave.open( wavfile, 'rb' )
    signal_length   = wf.getnframes()       # Signal length
    width           = wf.getsampwidth()     # Sample width

    return wf, signal_length, width