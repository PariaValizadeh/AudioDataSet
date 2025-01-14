import sounddevice as sd
import numpy as np
import os
import wave
import datetime
import json  # To handle appending labels as a list
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
        #self.device_id = getattr(hardware_config, "device_id", "default_device_id")
        self.device_id = hardware_config.device_id if hasattr(hardware_config,"device_id") else "default_device_id"
        if hasattr(hardware_config,"type"):
            self.type = hardware_config.type
        elif hasattr(config.type):
            self.type= config.type
        else:
            raise ValueError("the 'type' attribute is mssing in both hardware and config")
        self.channels = getattr(hardware_config, "channels", config.channels)
        self.gain = getattr(hardware_config, "gain", config.gain)

    def record(self):
        """
        Records multi-channel audio from a specified device.
        """
        print(f"Recording from device {self.device_id} for {self.config.duration} seconds.")
        print(f"using device ID:{self.device_id}")
        try:
            # Start recording
            recording = sd.rec(
                int(self.config.duration * self.config.sample_rate),
                samplerate=self.config.sample_rate,
                channels=self.channels,
                dtype='int16',
                device=self.device_id
            )
            sd.wait()  # Wait for the recording to finish
            return recording
        except Exception as e:
            print(f"An error occurred during recording {self.device_id}: {e}")
            return None

    def save(self, recording, filename):
    
        # Generate timestamp for the experiment folder (e.g., 2024-11-26_14-30-00)
        experiment_timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
        experiment_folder = os.path.join(self.config.output_dir, experiment_timestamp)

        # Create the experiment folder if it doesn't exist
        os.makedirs(experiment_folder, exist_ok=True)

        # Apply gain to recording
        recording = (recording * self.gain).astype(np.int16)

        # Get the current date and time for unique filenames
        current_time = datetime.datetime.now().strftime("%H-%M-%S")
        current_folder = os.path.join(experiment_folder, current_time)
        # create subfolder for the run
        os.makedirs(current_folder, exist_ok=True)

        # Save a file for each channel with metadata in the filename
        for channel in range(self.channels):
            # Generate filename using metadata
            filename = f"{experiment_timestamp}_{self.type}_ch{channel+1}_DOA{self.metadata['doa']}_elev{self.metadata['elevation']}_cat{'category'}_freq{self.metadata['frequency']}_gain{self.gain}_amp{self.metadata['amplitude']}_len{self.config.duration}_{current_time}.wav"
            
            # Construct file path in the experiment folder
            file_path = os.path.join(current_folder, filename)

            channel_data = recording[:, channel]
            with wave.open(file_path, "w") as wf:
                wf.setnchannels(1)  # Mono channel
                wf.setsampwidth(2)  # 16-bit PCM
                wf.setframerate(self.config.sample_rate)
                wf.writeframes(channel_data.tobytes())
            
            print(f"Saved channel {channel+1} to {file_path}")
        
   # Convert metadata to a JSON-serializable format
        metadata_serializable = OmegaConf.to_container(
            self.metadata, resolve=True, enum_to_str=True
        )

        # Create the label entry for this experiment
        label_entry = {
            "doa": metadata_serializable.get("doa"),
            "elevation": metadata_serializable.get("elevation"),
            "frequency": metadata_serializable.get("frequency"),
            "amplitude": metadata_serializable.get("amplitude"),
            "category": metadata_serializable.get("category"),
            "gain": self.gain,
            "duration": self.config.duration,
        }

        # Define the label file path
        label_file_path = os.path.join(self.config.output_dir, "experiment_labels.json")

        # Try to load the existing label file or initialize an empty list
        if os.path.exists(label_file_path):
            with open(label_file_path, 'r') as label_file:
                try:
                    label_data = json.load(label_file)
                except json.JSONDecodeError:
                    label_data = []  # If file exists but is empty or corrupted, initialize it
        else:
            label_data = []

        # Append the new label entry to the list
        label_data.append(label_entry)

        # Save the updated label data to the file
        with open(label_file_path, 'w') as label_file:
            json.dump(label_data, label_file, indent=4)

        print(f"Label file updated at {label_file_path}")