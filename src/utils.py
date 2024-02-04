import re
from typing import List


def str_to_list_formatter(text: str) -> List[str]:
    items = [line.strip() for line in text.split('\n\n')]

    # Compiling a regex pattern to match the leading numbering (e.g., "1. ")
    pattern = re.compile(r'^\d+\.\s*"')

    # Removing the leading numbers and unnecessary characters
    formatted = [pattern.sub('"', line.replace("\\'", "'"))
                 for line in items]
    return formatted
