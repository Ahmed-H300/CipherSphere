import textwrap
from config import GROUP_SIZE

# Encode


def encode(text):

    # Split text into substrings of [GROUP_SIZE] characters each
    encoded_texts = textwrap.wrap(text, width=GROUP_SIZE)

    # Add a space to the last substring if its length is less than [GROUP_SIZE] to make it equal to the [GROUP_SIZE]
    if len(encoded_texts[-1]) < 5:
        encoded_texts[-1] += " " * (5 - len(encoded_texts[-1]))

    return (encoded_texts)

