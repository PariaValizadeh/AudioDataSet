import os
import numpy as np
import wave
import logging
from AudioDataSet.recorder.base_recordermodule import AudioRecorder
from record_config import RecorderConfig

class RecorderHardware1(AudioRecorder):
    """
    Recorder for hardware 1 (e.g., ReSpeaker).
    """
    def __init__(self, config):
        super().__init__(config)
        self.device_id = config.device_id  # Device ID for hardware 1



class RecorderHardware2(AudioRecorder):
    """
    Recorder for hardware 2 (e.g., MiniDSP).
    """
    def __init__(self, config):
        super().__init__(config)
        self.device_id = config.device_id  # Device ID for hardware 2
