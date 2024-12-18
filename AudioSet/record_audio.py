import hydra
from omegaconf import DictConfig
from recorder.recorder_hardware import RecorderHardware
from recorder.data_labeler import DataLabeler
from utils.logger import get_logger
import logging
import time
import sys
import os
from configs.record_config import HardwareConfig

# Dynamically add the root of the project to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

# Optionally, add parent directories if required
sys.path.append(os.path.join(project_root, ".."))

# Setup logger
logging.basicConfig(level=logging.INFO)

@hydra.main(version_base="1.3", config_path="configs", config_name="record_config")
def record_audio(cfg: DictConfig):
    logger = get_logger(__name__)
    logger.info(f"Selected device: {cfg.selected_device}")

    # Extract the hardware configuration for the selected device
    hardware_config = cfg[cfg.selected_device]
    logger.info(f"Using hardware config: {hardware_config}")

    # Generate metadata dictionary
    metadata = {
        "doa": cfg.experiment_meta.doa,
        "elevation": cfg.experiment_meta.elevation,
        "selected_categories": cfg.experiment_meta.selected_categories,
        "frequency_range": cfg.experiment_meta.frequency_range,
        "amplitude_range": cfg.experiment_meta.amplitude_range,
        "experiment_id": cfg.experiment_meta.experiment_id,
        "category": cfg.experiment_meta.selected_categories,
        "frequency": cfg.experiment_meta.frequency,
        "amplitude": cfg.experiment_meta.amplitude,
    }

    # Dynamically select the recorder based on the selected device in the config
    if cfg.selected_device == "hardware1":
        logger.info("Initializing Recorder for ReSpeaker (Hardware 1)...")
        recorder = RecorderHardware(hardware_config, cfg.recorder, metadata)
    elif cfg.selected_device == "hardware2":
        logger.info("Initializing Recorder for MiniDSP (Hardware 2)...")
        recorder = RecorderHardware(hardware_config, cfg.recorder, metadata)
    else:
        raise ValueError(f"Unsupported device: {cfg.selected_device}")

    logger.info(f"Starting experiment: {cfg.experiment_meta.experiment_id}")
    
    # Record samples for the given sample count
    for i in range(cfg.experiment_meta.sample_count):
        logger.info(f"Recording sample {i+1}/{cfg.experiment_meta.sample_count}...")
        recording = recorder.record()
        if recording is not None:
            print("Calling save method ...")
            recorder.save(recording, f"sample_{i+1}")
            logger.info(f"Sample {i+1} saved successfully.")
        else:
            print("Recording failed; skipping save.")
        time.sleep(1)

if __name__ == "__main__":
    record_audio()

        