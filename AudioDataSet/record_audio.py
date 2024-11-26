import hydra
from omegaconf import DictConfig
from recorder.recorder_hardware import RecorderHardware1 ,RecorderHardware2

from recorder.data_labeler import DataLabeler
from utils.logger import get_logger
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)


@hydra.main(version_base="1.3", config_path="configs", config_name="record_config")
def record_audio(cfg: DictConfig):
    """
    Entry point for audio recording tasks.
    """
    logger = get_logger(__name__)
    logger.info(f"Selected device: {cfg.selected_device}")

    # Dynamically select the recorder based on the selected device in the config
    if cfg.selected_device == "hardware1":
        logger.info("Initializing Recorder for ReSpeaker (Hardware 1)...")
        recorder = RecorderHardware1(cfg.hardware1, cfg.recorder)
    elif cfg.selected_device == "hardware2":
        logger.info("Initializing Recorder for MiniDSP (Hardware 2)...")
        recorder = RecorderHardware2(cfg.hardware2, cfg.recorder)
    else:
        raise ValueError(f"Unsupported device: {cfg.selected_device}")

    # Record audio
    logger.info(f"Starting recording with {cfg.selected_device}...")
    data = recorder.record()

    # Save the recording
    logger.info("Saving recording...")
    recorder.save(data)

    # Label the data
    logger.info("Labeling the recorded data...")
    labeler = DataLabeler(cfg.recorder.labels_file)
    labeler.add_labels([cfg.selected_device], [data])

    logger.info(f"Recording task completed for {cfg.selected_device}!")

if __name__ == "__main__":
    record_audio()
