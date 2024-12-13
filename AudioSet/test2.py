import pyaudio

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,  # Set the sample rate to 44100 Hz
                input=True,
                frames_per_buffer=1024)
