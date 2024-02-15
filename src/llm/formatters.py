import re
from typing import List


def line_split_formatter(text: str) -> List[str]:
    items = [line.strip() for line in text.split('\n') if line]

    # Compiling a regex pattern to match the leading numbering (e.g., "1. ")
    pattern = re.compile(r'^\d+\.\s')
    # pattern = re.compile(r'^\d+\.\s*"') #  (e.g., "1. \"")

    # Removing leading numbers
    formatted_without_numebrs = [
        pattern.sub('"', line.replace("\'", "'"))
        for line in items
    ]

    # Cleaning quotes and empty lines
    formatted = [
        line.replace("'", "").replace('"', '')
        for line in formatted_without_numebrs if line
    ]
    return formatted


def add_author(quotes: List[str], author: str) -> List[str]:
    formatted = [
        f"\"{line}\"\n\n- {author} -"
        for line in quotes
    ]
    return formatted


def add_newlines(texts: List[str]) -> List[str]:
    # Pattern matches sentence-ending punctuation followed by a space or the end of the string
    pattern = re.compile(r'([.?!])(\s|$)')
    # Replace with the matched punctuation followed by two newlines and any following space
    return [re.sub(pattern, r'\1\n\n', text) for text in texts]
