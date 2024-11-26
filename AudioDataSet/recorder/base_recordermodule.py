from dataclasses import asdict
import torch
import random
from collections import Counter
import lightning as L
import pandas as pd
import hydra
from omegaconf import DictConfig
import logging

import os
import wave
import sounddevice as sd
import numpy as np
from configs.record_config import RecorderConfig
import datetime

class AudioRecorder2:
    """
    A base recorder module for handling hardwars and saving recorded data from Hardware.

    Attributes:

    Methods:
        __init__(config: RecorderConfig): Configuration object for the recorder.
        record(): Records multi-channel audio.
        save_channels(): Saves each channel of the recording as a separate WAV file.
        record_and_save(): Records audio and saves each channel.
        

    """


    def __init__(self, config: RecorderConfig):
        """
        Initialize the AudioRecorder with configuration.

        Args:
            config (RecorderConfig): Configuration object for the recorder.
        """
        self.config = config

    def record(self):
        """Records multi-channel audio."""
        print(f"Starting recording: {self.config.duration} seconds, {self.config.sample_rate} Hz, {self.config.channels} channels.")
        print("Available audio devices:")
        print(sd.query_devices())

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

    def save_channels(self, recording):
        """Saves each channel of the recording as a separate WAV file."""
        if recording is None:
            print("No recording data to save.")
            return

        # Ensure output directory exists
        os.makedirs(self.config.output_dir, exist_ok=True)

        # Apply gain and convert to 16-bit PCM
        recording = (recording * self.config.gain * 32767).astype(np.int16)
        for channel in range(self.config.channels):
            channel_data = recording[:, channel]
            file_name = os.path.join(self.config.output_dir, f"channel_{channel + 1}_gain_{self.config.gain:.2f}.wav")
            with wave.open(file_name, 'w') as wf:
                wf.setnchannels(1)  # Mono channel
                wf.setsampwidth(2)  # 16-bit PCM
                wf.setframerate(self.config.sample_rate)
                wf.writeframes(channel_data.tobytes())
            print(f"Channel {channel + 1} saved to {file_name} with gain {self.config.gain:.2f}")

    def record_and_save(self):
        """Records audio and saves each channel."""
        recording = self.record()
        self.save_channels(recording)




class AudioRecorder:
    """
    Base class for handling audio recording from hardware devices.
   
    Attributes:

    Methods:
        __init__(config: RecorderConfig): Configuration object for the recorder.
        record(): Records multi-channel audio.
        save_channels(): Saves each channel of the recording as a separate WAV file.
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

    def save(self, recording, sample_index):
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
