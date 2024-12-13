import os
import numpy as np
import wave
import logging
from recorder.base_recordermodule import AudioRecorder
from configs.record_config import RecorderConfig
import re



class RecorderHardware3(AudioRecorder):
    """
    Recorder for hardware 1 (e.g., ReSpeaker).
    """
    def __init__(self, hardware_config, recorder_config, metadata):
        super().__init__(recorder_config, metadata)  # Pass both config and metadata to the parent
        self.device_id = hardware_config.device_id
        self.channels = hardware_config.channels
        self.gain = hardware_config.gain
        print(f"Hardware config applied: device_id={self.device_id},channels={self.channels},gain={self.gain}")


class RecorderHardware1(AudioRecorder):
    def __init__(self, hardware_config, recorder_config, metadata):
        super().__init__(self,recorder_config, metadata)
        self.device_id = hardware_config.device_id
        self.channels = hardware_config.channels
        self.gain = hardware_config.gain
        print(f"Hardware config applied: device_id={self.device_id},channels={self.channels},gain={self.gain}")
 

    def extract_device_id(self, full_device_id):
        match = re.search(r"VID_([A-F0-9]+)&PID_([A-F0-9]+)", full_device_id)
        if match:
            return f"VID_{match.group(1)}&PID_{match.group(2)}"
        return full_device_id

class RecorderHardware2(AudioRecorder):
    def __init__(self, hardware_config, recorder_config, metadata):
        super().__init__(self,recorder_config, metadata)
        self.device_id = hardware_config.device_id
        self.channels = hardware_config.channels
        self.gain = hardware_config.gain
        print(f"Hardware config applied: device_id={self.device_id},channels={self.channels},gain={self.gain}")
 

    def extract_device_id(self, full_device_id):
        match = re.search(r"VID_([A-F0-9]+)&PID_([A-F0-9]+)", full_device_id)
        if match:
            return f"VID_{match.group(1)}&PID_{match.group(2)}"
        return full_device_id


