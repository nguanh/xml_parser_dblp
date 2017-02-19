import string
from unidecode import unidecode
from nameparser import HumanName
import re
from datetime import datetime

punctuation_dict = str.maketrans({key: None for key in (string.punctuation)})
whitespace_dict = str.maketrans({key: None for key in (string.whitespace.replace(" ", ""))})
ascii_dict = str.maketrans({key: None for key in (string.printable)})

# TODO interpret latex commands
def filter_latex(text):
    pass
    #\\[a-zA-z]+   matches all math commands \ddadad but not \jl{

def normalize_title(title, latex=False):

    # translate unicode characters to closest ascii characters
    ascii_decoded = unidecode(title)
    remove_punctuation = ascii_decoded.translate(punctuation_dict)
    remove_whitespace = remove_punctuation.translate(whitespace_dict)
    lowered = remove_whitespace.lower()
    only_one_space = lowered
    # by removing certain unicode characters we introduced multiple spaces, replace them by only on space
    while '  ' in only_one_space:
        only_one_space = only_one_space.replace('  ', ' ')

    return only_one_space.strip()


def split_authors(author_csv):
    authors_list = author_csv.split(";")
    # remove last entry since its always empty
    del authors_list[-1]
    return authors_list


def parse_authors(author_csv):
    authors_list = split_authors(author_csv)
    names = []
    for author in authors_list:
        name_dict = {'original': author}
        # remove dblp numbers from name
        stripped_numbers = re.sub(r'\d{4}', '', author).strip()
        # try to find last name
        num_names = len(author.split(" "))
        name_dict['real'] = stripped_numbers
        # if author name contains only one name, it will serve the purpose of the last name
        if num_names == 1:
            last_name = stripped_numbers
            name_dict['block'] = normalize_title(last_name) + ","
        else:
            name = HumanName(stripped_numbers).as_dict()
            norm_last_name = normalize_title(name['last'])
            norm_first_name = normalize_title(name['first'])[0] if len(name['first']) > 0 else ''
            name_dict['block'] = norm_last_name + "," + norm_first_name

        names.append(name_dict)

    return names


def parse_pages(pages, separator="-"):
    result = pages.split(separator)
    # publication contains only one page
    if len(result) == 1:
        return [result[0], result[0]]
    if len(result) == 2:
        return [result[0], result[1]]
    #TODO log invalid page
    return [None, None]
