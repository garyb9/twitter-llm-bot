import os
import configparser
from transformers import AutoModelForCausalLM, AutoTokenizer

config = configparser.ConfigParser()
config_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../models_config.ini'))
config.read(config_path)

MODELS_DIR = os.path.abspath(os.path.join(
    config_path, config['General']['directory']))
MODELS = config['Models']


def load_models():
    print(f"Syncing Models")
    for name, hf_id in MODELS.items():
        model_dir = os.path.join(MODELS_DIR, name)
        if not os.path.exists(model_dir):
            print(f"Downloading {name} model...")
            model = AutoModelForCausalLM.from_pretrained(hf_id)
            tokenizer = AutoTokenizer.from_pretrained(hf_id)

            model.save_pretrained(model_dir)
            tokenizer.save_pretrained(model_dir)
            print(f"{name} downloaded.")
        else:
            print(f"{name} already exists, skipping download.")


if __name__ == "__main__":
    load_models()
