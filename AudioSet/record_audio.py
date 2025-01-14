import hydra
from omegaconf import DictConfig, OmegaConf
import os
import time
#python audioset/record_audio.py +experiment=experiment/audiorecord/class1.yaml

@hydra.main(version_base="1.3", config_path="configs", config_name="record_config")
def record_audio(cfg: DictConfig):
    print("\n=== Final Configuration ===")
    print(OmegaConf.to_yaml(cfg))
    print("===========================\n")

    # Initialize recording
    recorder = None
    if cfg.selected_device == "hardware1":
        print(f"Using Recorder for {cfg.hardware1.type} (Hardware 1)...")
        recorder = cfg.hardware1
    elif cfg.selected_device == "hardware2":
        print(f"Using Recorder for MiniDSP (Hardware 2)...")
        recorder = cfg.hardware2
    else:
        raise ValueError(f"Unsupported device: {cfg.selected_device}")

    # Iterate over sample count
    for i in range(cfg.experiment_meta.sample_count):
        print(f"Recording sample {i+1} with settings:")
        print(f"DOA: {cfg.experiment_meta.doa}, Frequency: {cfg.experiment_meta.frequency}, Amplitude: {cfg.experiment_meta.amplitude}")
        time.sleep(1)  # Simulate recording
        print(f"Sample {i+1} recorded successfully!\n")

if __name__ == "__main__":
    record_audio()