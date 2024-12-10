import sounddevice as sd
import numpy as np
import os
import wave
import datetime
class AudioRecorder:
    """
    Base class for handling audio recording from hardware devices.

    Attributes:
        config (RecorderConfig): Configuration for the recorder.
        metadata (dict): Metadata information for the experiment.
        channels (int): Number of channels to record.
        device_id (str): Device ID for the hardware.
        gain (float): Gain value for the device.

    Methods:
        __init__(hardware_config, config, metadata): Initializes the recorder with hardware info, config, and metadata.
        record(): Records multi-channel audio.
        save(): Saves each channel of the recording with metadata.
    """

    def __init__(self, hardware_config, config, metadata):
        self.config = config
        self.metadata = metadata
        
        # Dynamically fetch hardware-specific attributes
        self.device_id = getattr(hardware_config, "device_id", "default_device_id")
        self.channels = getattr(hardware_config, "channels", config.channels)
        self.gain = getattr(hardware_config, "gain", config.gain)

    def record(self):
        """
        Records multi-channel audio from a specified device.
        """
        print(f"Recording from device {self.device_id} for {self.config.duration} seconds.")
        try:
            # Start recording
            recording = sd.rec(
                int(self.config.duration * self.config.sample_rate),
                samplerate=self.config.sample_rate,
                channels=self.channels,
                dtype='float32',
                device=self.device_id
            )
            sd.wait()  # Wait for the recording to finish
            return recording
        except Exception as e:
            print(f"An error occurred during recording: {e}")
            return None

    def save(self, recording, filename):
        """
        Saves each channel's recording with metadata (DOA, frequency, etc.) as part of the filename.
        """
        os.makedirs(self.config.output_dir, exist_ok=True)

        # Apply gain to recording
        recording = (recording * self.gain * 32767).astype(np.int16)

        # Get the current date and time for unique filenames
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Save a file for each channel with metadata in the filename
        for channel in range(self.channels):
            # Generate filename using metadata
            filename = f"{self.metadata['experiment_id']}_{self.device_id}_ch{channel+1}_DOA{self.metadata['doa']}_elev{self.metadata['elevation']}_cat{self.metadata['category']}_freq{self.metadata['frequency']}_gain{self.gain}_amp{self.metadata['amplitude']}_len{self.config.duration}_{current_time}.wav"
            file_path = os.path.join(self.config.output_dir, filename)

            channel_data = recording[:, channel]
            with wave.open(file_path, "w") as wf:
                wf.setnchannels(1)  # Mono channel
                wf.setsampwidth(2)  # 16-bit PCM
                wf.setframerate(self.config.sample_rate)
                wf.writeframes(channel_data.tobytes())
            print(f"Saved channel {channel+1} to {file_path}")

class AudioRecorder2:
    """
    Base class for handling audio recording from hardware devices.

    Attributes:
        config (RecorderConfig): Configuration for the recorder.
        metadata (dict): Metadata information for the experiment.
        channels (int): Number of channels to record.
        device_id (str): Device ID for the hardware.
        gain (float): Gain value for the device.

    Methods:
        __init__(config, metadata): Initializes the recorder with given config and metadata.
        record(): Records multi-channel audio.
        save(): Saves each channel of the recording with metadata.
        record_and_save(): Records audio and saves each channel.
    """

    def __init__(self, config, metadata):
        self.config = config
        self.metadata = metadata
        self.channels = self.config.channels
        self.device_id = self.config.device_id
        self.gain = self.config.gain

    def record(self):
        """
        Records multi-channel audio from a specified device.
        """
        print(f"Recording from device {self.device_id} for {self.config.duration} seconds.")
        try:
            # Start recording
            recording = sd.rec(
                int(self.config.duration * self.config.sample_rate),
                samplerate=self.config.sample_rate,
                channels=self.config.channels,
                dtype='float32',
                device=self.config.device
            )
            sd.wait()  # Wait for the recording to finish
            return recording
        except Exception as e:
            print(f"An error occurred during recording: {e}")
            return None

    def save(self, recording, filename):
        """
        Saves each channel's recording with metadata (DOA, frequency, etc.) as part of the filename.
        """
        os.makedirs(self.config.output_dir, exist_ok=True)

        # Apply gain to recording
        recording = (recording * self.gain * 32767).astype(np.int16)

        # Get the current date and time for unique filenames
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Save a file for each channel with metadata in the filename
        for channel in range(self.channels):
            # Generate filename using metadata
            filename = f"{self.metadata['experiment_id']}_{self.device_id}_ch{channel+1}_DOA{self.metadata['doa']}_elev{self.metadata['elevation']}_cat{self.metadata['category']}_freq{self.metadata['frequency']}_gain{self.gain}_amp{self.metadata['amplitude']}_len{self.config.duration}_{current_time}.wav"
            file_path = os.path.join(self.config.output_dir, filename)

            channel_data = recording[:, channel]
            with wave.open(file_path, "w") as wf:
                wf.setnchannels(1)  # Mono channel
                wf.setsampwidth(2)  # 16-bit PCM
                wf.setframerate(self.config.sample_rate)
                wf.writeframes(channel_data.tobytes())
            print(f"Saved channel {channel+1} to {file_path}")