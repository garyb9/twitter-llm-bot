import os
import re
import json
import random
from typing import List

# Load prompts configuration
prompts_config_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../data/prompts_config.json'))

with open(prompts_config_path, 'r') as file:
    prompts_config = json.load(file)

# Function to prepare a random prompt


def prepare_random_prompt(category: str = None):
    if not category:
        category = random.choice(list(prompts_config.keys()))
    prompt = random.choice(prompts_config[category])
    message_template = random.choice(prompt['messages'])
    input_var = {var: random.choice(
        values) for var, values in prompt['input_variables'].items()}
    message_content = message_template['content'].format(**input_var)
    return {
        "role": message_template['role'],
        "content": message_content
    }


def str_to_list_formatter(text: str) -> List[str]:
    items = [line.strip() for line in text.split('\n\n')]

    # Compiling a regex pattern to match the leading numbering (e.g., "1. ")
    pattern = re.compile(r'^\d+\.\s*"')

    # Removing the leading numbers and unnecessary characters
    formatted = [pattern.sub('"', line.replace("\\'", "'"))
                 for line in items]
    return formatted
