import hydra
from omegaconf import DictConfig, OmegaConf
from recorder.recorder_hardware import RecorderHardware
from recorder.data_labeler import DataLabeler
from utils.logger import get_logger
import logging
import time
import sys
import os
from recorder.record_config import HardwareConfig,RecorderConfig,ExperimentConfig
import pyrootutils
from pathlib import Path
'''
# Dynamically add the root of the project to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

# Optionally, add parent directories if required
sys.path.append(os.path.join(project_root, ".."))

# Setup logger
logging.basicConfig(level=logging.INFO)
'''

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git"],
    pythonpath=True,
    dotenv=True,
)

_HYDRA_PARAMS = {
    "version_base": None,
    "config_path": str(root / "configs"),
    "config_name": "config.yaml",
}


#@hydra.main(version_base="1.3", config_path="/workspace/configs/datamodule", config_name="config")
# @utils.register_custom_resolvers(**_HYDRA_PARAMS)
@hydra.main(**_HYDRA_PARAMS)
def record_audio(cfg: DictConfig):
    logger = get_logger(__name__)
    logger.info("Final configuration")
    #logger.info(OmegaConf.to_yaml(cfg))
    logger.info(f"Loaded configuration: {OmegaConf.to_yaml(cfg)}")

    
    logger.info(f"Selected device: {cfg.selected_device}")
    

    # Extract the hardware configuration for the selected device
    hardware_config = cfg.hardware_config.hardware_config[cfg.selected_device]
    recorder_config = cfg.recorder_config.recorder
    experiment_config = cfg.experiment_config
    logger.info(f"Using hardware config: {hardware_config}")
    logger.info(f"Using recorder config: {recorder_config}")
    recorder_config.channels= hardware_config.channels

    # Generate metadata dictionary
    metadata = {
        "doa": experiment_config.doa,
        "elevation": experiment_config.elevation,
        "selected_categories": experiment_config.selected_categories,
        "frequency_range": experiment_config.frequency_range,
        "amplitude_range": experiment_config.amplitude_range,
        "experiment_id": experiment_config.experiment_id,
        "category": experiment_config.selected_categories,
        "frequency": experiment_config.frequency,
        "amplitude": experiment_config.amplitude,

        

    }

    # Dynamically select the recorder based on the selected device in the config
    if cfg.selected_device == "hardware1":
        logger.info("Initializing Recorder for ReSpeaker (Hardware 1)...")
        recorder = RecorderHardware(hardware_config, recorder_config, metadata)
    elif cfg.selected_device == "hardware2":
        logger.info("Initializing Recorder for MiniDSP (Hardware 2)...")
        recorder = RecorderHardware(hardware_config, recorder_config, metadata)
    else:
        raise ValueError(f"Unsupported device: {cfg.selected_device}")

    logger.info(f"Starting experiment: {experiment_config.experiment_id}")
    
    # Record samples for the given sample count
    for i in range(experiment_config.sample_count):
        logger.info(f"Recording sample {i+1}/{experiment_config.sample_count}...")
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

        