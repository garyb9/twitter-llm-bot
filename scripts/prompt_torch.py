from setup_env import setup

setup()
import torch
from hf_models.model_loader import ModelLoader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_loader = ModelLoader()
model_loader.download_models_pretrained()

model = AutoModelForSeq2SeqLM.from_pretrained(
    model_loader.models_pretrained_dir, local_files_only=True
)
tokenizer = AutoTokenizer.from_pretrained(
    model_loader.models_pretrained_dir, local_files_only=True
)

# Set the device to GPU if available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define a simple text prompt
prompt = "Once upon a time, in a land far, far away, there was a"

# Generate text using the model
input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
output = model.generate(
    input_ids,
    max_length=100,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    top_k=50,
    top_p=0.95,
)

# Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated Text:")
print(generated_text)
