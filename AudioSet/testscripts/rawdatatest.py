import sounddevice as sd
import numpy as np
import wave
from queue import Queue

# Configuration constants
RESPEAKER_RATE = 16000  # Sample rate
RESPEAKER_CHANNELS = 6  # Number of channels
RESPEAKER_WIDTH = 2  # Sample width in bytes (2 bytes = 16-bit)
RECORD_SECONDS = 3  # Recording duration in seconds
WAVE_OUTPUT_FILENAME = "output_channel_{}.wav"  # Template for output filenames

# Prepare frames list for each channel
frames = [[] for _ in range(RESPEAKER_CHANNELS)]
q = Queue()

# Recording callback function
def callback(indata, frames_per_buffer, time, status):
    if status:
        print(status)
    # Put the incoming data into the queue for later processing
    q.put(indata.copy())

# Open the audio stream with sounddevice
with sd.InputStream(
    channels=RESPEAKER_CHANNELS,
    samplerate=RESPEAKER_RATE,
    dtype='int16',  # 16-bit integer format for audio
    callback=callback
):
    print("* recording")
    sd.sleep(RECORD_SECONDS * 1000)  # Record for the specified duration (in milliseconds)
    print("* done recording")

# Process data from the queue after recording
while not q.empty():
    indata = q.get()
    for channel in range(RESPEAKER_CHANNELS):
        channel_data = indata[:, channel]  # Extract data for each channel
        frames[channel].append(channel_data)

# Save each channel's data into a separate WAV file
for channel in range(RESPEAKER_CHANNELS):
    output_filename = WAVE_OUTPUT_FILENAME.format(channel)
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono channel (each channel is saved separately)
        wf.setsampwidth(RESPEAKER_WIDTH)  # 2 bytes (16-bit depth)
        wf.setframerate(RESPEAKER_RATE)  # Sample rate

        # Concatenate all frames from the current channel and write them to the file
        channel_audio_data = np.concatenate(frames[channel])  # Flatten the frames list into one array
        wf.writeframes(channel_audio_data.tobytes())  # Write audio data to file

    print(f"Channel {channel} saved as {output_filename}")
