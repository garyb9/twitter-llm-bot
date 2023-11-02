import os
import json
import logging
import subprocess
from transformers import AutoModelForCausalLM, AutoTokenizer

"""
    Model Loader loads models from Hugging Face model hub: 
    https://huggingface.co/models
    
    Suggestion - its better to use `download_models_git()` if low on resources,
    since git has better handling of downloading of large file than hugging face's `from_pretrained` downloader.
"""


class ModelLoader():
    def __init__(self) -> None:
        config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../models_config.json'))
        with open(config_path, 'r') as file:
            config = json.load(file)

        self.models = {}
        self.models_config_dir = os.getenv("HUGGINGFACE_HUB_CACHE") or \
            os.getenv("TRANSFORMERS_CACHE") or \
            os.path.abspath(os.path.join(
                os.path.dirname(__file__), '../models/'))
        self.models_pretrained_dir = os.path.join(
            self.models_config_dir, 'pretrained')
        self.models_config = config['models']
        for model_type in self.models_config.keys():
            model_dir_by_type = os.path.join(
                self.models_config_dir, model_type)
            if not os.path.exists(model_dir_by_type):
                os.makedirs(model_dir_by_type)
            for model_repo in self.models_config[model_type]:
                parts = model_repo.split("/")
                name = parts[-1]
                directory = os.path.join(
                    model_dir_by_type, name)
                self.models[name] = {
                    "id": "/".join(parts[-2:]),
                    "type": model_type,
                    "repository": model_repo,
                    "directory": directory
                }
        logging.info(f"Models configured: {json.dumps(self.models, indent=4)}")

    def download_models_pretrained(self):
        logging.info(f"Downloading Models from config file")
        for name, details in self.models.items():
            try:
                directory = details['directory']
                if os.path.exists(directory):
                    logging.info(
                        f"Model {name} found in {directory}, skipping download")
                else:
                    logging.info(f"Downloading {name} model...")
                    model = AutoModelForCausalLM.from_pretrained(details['id'])
                    tokenizer = AutoTokenizer.from_pretrained(details['id'])
                    logging.info(f"Saving pretrained {name} model...")
                    model.save_pretrained(directory)
                    tokenizer.save_pretrained(directory)
                    logging.info(f"{name} downloaded.")
            except subprocess.CalledProcessError as e:
                logging.info(f"Error getting model: {name}")

        logging.info(f"Done loading models")

    def download_models_git(self):
        logging.info(f"Downloading Models from config file")
        for name, details in self.models.items():
            try:
                directory = details['directory']
                if os.path.exists(directory):
                    logging.info(
                        f"Model {name} found in {directory}, skipping download")
                else:
                    os.chdir(directory)
                    logging.info(f"Changed to {directory}")
                    git_command = f"git clone {details['repository']}"
                    subprocess.run(git_command, shell=True, check=True)
                    logging.info("Git command executed successfully.")

                    # Load the model and tokenizer
                    logging.info(f"Loading model and tokenizer of {name}")
                    model = AutoModelForCausalLM.from_pretrained(
                        directory, local_files_only=True)
                    tokenizer = AutoTokenizer.from_pretrained(
                        directory, local_files_only=True)

                    # Save the model and tokenizer to the pretrained directory
                    pretrained_dir = os.path.join(directory, "pretrained")
                    logging.info(f"Saving pretrained {name} model...")
                    model.save_pretrained(pretrained_dir)
                    tokenizer.save_pretrained(pretrained_dir)

            except subprocess.CalledProcessError as e:
                logging.info(f"Error getting model {name}: {e}")
        logging.info(f"Done loading models")


def sample_prompt_test(model_loader: ModelLoader):
    model = AutoModelForCausalLM.from_pretrained(
        model_loader.models_pretrained_dir, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(
        model_loader.models_pretrained_dir, local_files_only=True)

    # Set the device to GPU if available, otherwise use CPU
    import torch
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Define a simple text prompt
    prompt = "Once upon a time, in a land far, far away, there was a"

    # Generate text using the model
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output = model.generate(input_ids, max_length=100, num_return_sequences=1,
                            no_repeat_ngram_size=2, top_k=50, top_p=0.95)

    # Decode and print the generated text
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print("Generated Text:")
    print(generated_text)


if __name__ == "__main__":
    import setup_env
    model_loader = ModelLoader()
    model_loader.download_models_git()
    # sample_prompt_test(model_loader)
