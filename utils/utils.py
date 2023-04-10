import textwrap
from config import GROUP_SIZE

# Encode Word
def encode_word(word):

    encode_word = 0
    for i, char in enumerate(reversed(word)):
        encode_word += (map_char(char) * (37 ** i))
    return (encode_word)

# Map Character
def map_char(char):

    if char.isalpha():
        char = char.lower()
        return ((ord(char) - ord('a')) + 10)
    elif char.isdigit():
        return (ord(char) - ord('0'))
    else:
        return (36)

# Map integer
def map_int(value):
    
    if value < 10:
        return (chr(value + ord('0')))
    elif value < 36:
        return (chr(value - 10 + ord('a')))
    else:
        return (' ')

# Decode Word
def decode_word(encode_word):

    decode_word = ""
    while (encode_word > 0):
        decode_word = map_int(encode_word % 37) + decode_word
        encode_word //= 37
    return (decode_word)

# Split Text
def split_text(text):

    # Split text into substrings of [GROUP_SIZE] characters each
    splited_texts = [text[i:i+GROUP_SIZE] for i in range(0, len(text), GROUP_SIZE)]

    # Add a space to the last substring if its length is less than [GROUP_SIZE] to make it equal to the [GROUP_SIZE]
    if len(splited_texts[-1]) < GROUP_SIZE:
        splited_texts[-1] += " " * (GROUP_SIZE - len(splited_texts[-1]))

    return (splited_texts)

# Combine Text
def combine_text(splited_texts):
    
    # Join the substrings into a single string
    combined_text = "".join(splited_texts)

    # Remove the spaces from the end of the string
    combined_text = combined_text.rstrip()

    return (combined_text)

# Encode Text
def encode_text(text):
    
    # Split text into substrings of [GROUP_SIZE] characters each
    splited_texts = split_text(text)

    # Encode each substring
    encoded_texts = []
    for splited_text in splited_texts:
        encoded_texts.append(encode_word(splited_text))

    return (encoded_texts)

# Decode Text
def decode_text(encoded_texts):
    
    # Decode each substring
    decoded_texts = []
    for encoded_text in encoded_texts:
        decoded_texts.append(decode_word(encoded_text))

    # Join the substrings into a single string
    combined_text = combine_text(decoded_texts)

    return (combined_text)

