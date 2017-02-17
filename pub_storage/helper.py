import string
from unidecode import unidecode
punctuation_dict = str.maketrans({key: None for key in (string.punctuation)})
whitespace_dict = str.maketrans({key: None for key in (string.whitespace.replace(" ", ""))})

#TODO strip latex commands
def normalize_title(title):

    remove_punctuation = title.translate(punctuation_dict)
    remove_whitespace = remove_punctuation.translate(whitespace_dict)
    ascii_decoded = unidecode(remove_whitespace)
    #translate unicode characters to closest ascii characters
    lowered = ascii_decoded.lower()
    stripped = lowered.strip()
    return stripped

