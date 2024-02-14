import re
from typing import List


def line_split_formatter(text: str) -> List[str]:
    items = [line.strip() for line in text.split('\n')]

    # Compiling a regex pattern to match the leading numbering (e.g., "1. ")
    pattern = re.compile(r'^\d+\.\s*"')

    # Removing leading numbers
    formatted_without_numebrs = [
        pattern.sub('"', line.replace("\'", "'"))
        for line in items
    ]

    # Cleaning quotes
    formatted = [
        line.replace("'", "").replace('"', '')
        for line in formatted_without_numebrs
    ]
    return formatted


# def clean_quotes(quotes: List[str]) -> List[str]:
#     # Removing the leading numbers and unnecessary characters
#     formatted = [
#         pattern.sub('"', line.replace("\'", "'"))
#         for line in items
#     ]

#     return formatted


def add_author(quotes: List[str], author: str):
    formatted = [
        f"\"{line}\"\n\n- {author} -"
        for line in quotes
    ]
    return formatted
