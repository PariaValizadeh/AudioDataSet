import sounddevice as sd
import numpy as np
import wave

duration = 5  # seconds
sample_rate = 16000
channels = 2
device = 'hw:1,0'  # Adjust as per your device

print("Recording...")
recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=channels,
    dtype='int16',
    device=device
)
sd.wait()
print("Recording complete.")

# Save to a WAV file
file_name = "test.wav"
with wave.open(file_name, 'w') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(2)  # 2 bytes for 16-bit audio
    wf.setframerate(sample_rate)
    wf.writeframes(recording.tobytes())

print(f"Saved recording to {file_name}")
