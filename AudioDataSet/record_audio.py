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
    logger = logging.getLogger(__name__)
    logger.info(f"Starting experiment {cfg.experiment_meta.experiment_id}...")

    # Metadata for the experiment
    metadata = {
        'experiment_id': cfg.experiment_meta.experiment_id,
        'doa': cfg.experiment_meta.doa_range,
        'elevation': cfg.experiment_meta.elevation_range,
        'category': cfg.experiment_meta.category_list[0],  # Example, could be dynamic based on each experiment
        'frequency': cfg.experiment_meta.frequency_range,
        'gain': cfg.recorder.gain,
        'amplitude': 1.0,  # Example, amplitude could be dynamic as well
        'length': cfg.recorder.duration
    }

    # Initialize the recorder based on the selected device
    if cfg.hardware1.type == "ReSpeaker":
        logger.info("Initializing Recorder for ReSpeaker...")
        recorder = RecorderHardware1(cfg.hardware1, metadata)
    elif cfg.hardware2.type == "MiniDSP":
        logger.info("Initializing Recorder for MiniDSP...")
        recorder = RecorderHardware2(cfg.hardware2, metadata)
    else:
        raise ValueError(f"Unsupported device: {cfg.hardware1.type}")

    # Record audio
    logger.info(f"Starting recording for device {cfg.hardware1.device_id}...")
    recording = recorder.record()

    # Save the recording
    recorder.save(recording, sample_index=1)

    # Label the data
    labeler = DataLabeler(cfg.recorder.labels_file)
    labeler.add_labels([metadata], [{'filename': f"{metadata['experiment_id']}_file", **metadata}])

    logger.info(f"Experiment {cfg.experiment_meta.experiment_id} completed!")

if __name__ == "__main__":
    record_audio()
