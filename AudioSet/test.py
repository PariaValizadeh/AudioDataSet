import sounddevice as sd

# Explicitly select your device
device_id = 1  # Replace with your device name from `sd.query_devices()`

try:
    # Start a basic recording
    duration = 5  # seconds
    samplerate = 16000
    channels = 6
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, device=device_id)
    sd.wait()  # Wait for recording to finish
    print("Recording successful!")
except Exception as e:
    print(f"Error: {e}")
