import os
import hydra
import lightning as L
from omegaconf import OmegaConf, open_dict
from omegaconf.errors import ConfigAttributeError
import json
from AudioSet import utils
import pyrootutils
from pathlib import Path

# Logger setup
log = utils.get_pylogger(__name__)

# Set up the root of the project
root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git"],
    pythonpath=True,
    dotenv=True,
)

# Define Hydra configuration parameters
_HYDRA_PARAMS = {
    "version_base": None,
    "config_path": str(root / "configs"),  # Path to the config directory
    "config_name": "train.yaml",           # Base config file
}

# The main function where you train and evaluate the model
@hydra.main(**_HYDRA_PARAMS)
def train(cfg):
    log.info("Using config: \n%s", OmegaConf.to_yaml(cfg))

    # Setup paths and create directories if needed
    log.info(f"Dataset path: <{os.path.abspath(cfg.paths.dataset_path)}>")
    os.makedirs(cfg.paths.dataset_path, exist_ok=True)

    log.info(f"Log path: <{os.path.abspath(cfg.paths.log_dir)}>")
    os.makedirs(cfg.paths.log_dir, exist_ok=True)

    log.info(f"Root Dir: <{os.path.abspath(cfg.paths.log_dir)}>")
    log.info(f"Work Dir: <{os.path.abspath(cfg.paths.work_dir)}>")
    log.info(f"Output Dir: <{os.path.abspath(cfg.paths.output_dir)}>")
    log.info(f"Background Dir: <{os.path.abspath(cfg.paths.background_path)}>")

    log.info(f"Seed everything with <{cfg.seed}>")
    L.seed_everything(cfg.seed)

    # Initialize the data module
    log.info(f"Instantiate datamodule <{cfg.datamodule._target_}>")
    datamodule = hydra.utils.instantiate(cfg.datamodule)
    datamodule.prepare_data()

    # Instantiate the logger
    log.info(f"Instantiate logger")
    logger = utils.instantiate_loggers(cfg.get("logger"))

    # Set up callbacks
    log.info(f"Instantiate callbacks")
    callbacks = utils.instantiate_callbacks(cfg["callbacks"])

    # Initialize the trainer
    log.info(f"Instantiate trainer <{cfg.trainer._target_}>")
    trainer = hydra.utils.instantiate(cfg.trainer, callbacks=callbacks, logger=logger)

    # Optionally handle pretrain info
    pretrain_info = None
    try:
        pretrain_info = cfg.module.network.model.pretrain_info
    except ConfigAttributeError:
        log.info("pretrain_info does not exist, using None instead")

    # Setup model configuration
    log.info(f"Instantiate model <{cfg.module.network.model._target_}>")
    with open_dict(cfg):
        cfg.module.metrics["num_labels"] = datamodule.num_classes
        cfg.module.network.model["num_classes"] = datamodule.num_classes
        if cfg.module.network.model.get("classifier"):
            cfg.module.network.model.classifier["num_classes"] = datamodule.num_classes

    # Instantiate the model
    model = hydra.utils.instantiate(
        cfg.module,
        num_epochs=cfg.trainer.max_epochs,
        len_trainset=datamodule.len_trainset,
        batch_size=datamodule.loaders_config.train.batch_size,
        pretrain_info=pretrain_info,
    )

    object_dict = {
        "cfg": cfg,
        "datamodule": datamodule,
        "model": model,
        "callbacks": callbacks,
        "logger": logger,
        "trainer": trainer,
    }

    log.info("Logging Hyperparams")
    utils.log_hyperparameters(object_dict)

    # Training process
    if cfg.get("train"):
        log.info(f"Starting training")
        ckpt = cfg.get("ckpt_path")
        if ckpt:
            log.info(f"Resume training from checkpoint {ckpt}")
        else:
            log.info("No checkpoint found. Training from scratch!")

        trainer.fit(model=model, datamodule=datamodule, ckpt_path=cfg.get("ckpt_path"))

    train_metrics = trainer.callback_metrics

    # Testing process
    if cfg.get("test"):
        log.info(f"Starting testing")
        ckpt_path = trainer.checkpoint_callback.best_model_path
        if ckpt_path == "":
            if cfg.get("ckpt_path"):
                ckpt_path = cfg.ckpt_path
            else:
                log.warning("No checkpoint found. Using current weights for testing")
                ckpt_path = None
        else:
            log.info(
                f"The best checkpoint for {cfg.callbacks.model_checkpoint.monitor} "
                f" is {trainer.checkpoint_callback.best_model_score} "
                f" and saved in {ckpt_path}"
            )
        trainer.test(model=model, datamodule=datamodule, ckpt_path=ckpt_path)

    test_metrics = trainer.callback_metrics

    # Save state dicts
    if cfg.get("save_state_dict"):
        log.info(f"Saving state dicts")
        utils.save_state_dicts(
            trainer=trainer,
            model=model,
            dirname=cfg.paths.output_dir,
            **cfg.extras.state_dict_saving_params,
        )

    # Dump metrics to disk
    if cfg.get("dump_metrics"):
        log.info(f"Dumping final metrics locally to {cfg.paths.output_dir}")
        metric_dict = {**train_metrics, **test_metrics}

        metric_dict = [
            {"name": k, "value": v.item() if hasattr(v, "item") else v}
            for k, v in metric_dict.items()
        ]

        file_path = os.path.join(cfg.paths.output_dir, "finalmetrics.json")
        with open(file_path, "w") as json_file:
            json.dump(metric_dict, json_file)

    utils.close_loggers()


if __name__ == "__main__":
    # Set TensorFlow logging level
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    train()
