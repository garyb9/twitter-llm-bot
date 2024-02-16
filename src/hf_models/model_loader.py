import os
import json
import logging
import subprocess
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class ModelLoader:
    def __init__(self) -> None:
        config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../models_config.json")
        )
        with open(config_path, "r") as file:
            config = json.load(file)

        self.models = {}
        self.models_config_dir = (
            os.getenv("HUGGINGFACE_HUB_CACHE")
            or os.getenv("TRANSFORMERS_CACHE")
            or os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/"))
        )
        self.models_pretrained_dir = os.path.join(self.models_config_dir, "pretrained")
        self.models_config = config["models"]
        for model_type in self.models_config.keys():
            model_dir_by_type = os.path.join(self.models_config_dir, model_type)
            if not os.path.exists(model_dir_by_type):
                os.makedirs(model_dir_by_type)
            for model_repo in self.models_config[model_type]:
                parts = model_repo.split("/")
                name = parts[-1]
                directory = os.path.join(model_dir_by_type, name)
                self.models[name] = {
                    "id": "/".join(parts[-2:]),
                    "type": model_type,
                    "repository": model_repo,
                    "directory": directory,
                }
        logging.info(f"Models configured: {json.dumps(self.models, indent=4)}")

    def download_models_pretrained(self):
        logging.info("Downloading Models from config file")
        for name, details in self.models.items():
            try:
                directory = details["directory"]
                if os.path.exists(directory):
                    logging.info(
                        f"Model {name} found in {directory}, skipping download"
                    )
                else:
                    logging.info(f"Downloading {name} model...")
                    model = AutoModelForSeq2SeqLM.from_pretrained(details["id"])
                    tokenizer = AutoTokenizer.from_pretrained(details["id"])
                    logging.info(f"Saving pretrained {name} model...")
                    model.save_pretrained(directory)
                    tokenizer.save_pretrained(directory)
                    logging.info(f"{name} downloaded.")
            except subprocess.CalledProcessError as e:
                logging.info(f"Error getting model: {name} -> {e}")

        logging.info("Done loading models")

    def download_models_git(self):
        logging.info("Downloading Models from config file")
        for name, details in self.models.items():
            try:
                directory = details["directory"]
                if os.path.exists(directory):
                    logging.info(
                        f"Model {name} found in {directory}, skipping download"
                    )
                else:
                    os.chdir(directory)
                    logging.info(f"Changed to {directory}")
                    git_command = f"git clone {details['repository']}"
                    subprocess.run(git_command, shell=True, check=True)
                    logging.info("Git command executed successfully.")

                    # Load the model and tokenizer
                    logging.info(f"Loading model and tokenizer of {name}")
                    model = AutoModelForSeq2SeqLM.from_pretrained(
                        directory, local_files_only=True
                    )
                    tokenizer = AutoTokenizer.from_pretrained(
                        directory, local_files_only=True
                    )

                    # Save the model and tokenizer to the pretrained directory
                    pretrained_dir = os.path.join(directory, "pretrained")
                    logging.info(f"Saving pretrained {name} model...")
                    model.save_pretrained(pretrained_dir)
                    tokenizer.save_pretrained(pretrained_dir)

            except subprocess.CalledProcessError as e:
                logging.info(f"Error getting model {name}: {e}")
        logging.info("Done loading models")
