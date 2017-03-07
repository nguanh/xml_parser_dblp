from pub_storage.helper import parse_pages, split_authors
import re


def generate_empty_mapping():
    return{
        "local_url": "",
        "publication": {
            "url_id": None,
            "cluster_id": None,
            "differences": None,
            "title": None,  # for title and cluster name
            "pages": None,
            "note": None,
            "doi": None,
            "abstract": None,
            "copyright": None,
            "date_added": None,
            "date_published": None,
            "volume": None,
            "number": None,
            "study_field_ids": None,
            "author_ids": None,
            "type_ids": None,
            "keyword_ids": None,
            "pub_source_ids": None,
        },
        "pub_release": {
            "key": None,
            "series": None,
            "edition": None,
            "location": None,
            "publisher": None,
            "institution": None,
            "school": None,
            "address": None,
            "isbn": None,
            "howpublished": None,
            "book_title": None,
            "journal": None,
        },
        "authors": [],
        "study_fields": [],
        "types": None,
        "keywords": [],
    }


"""
SAMPLE AUTHORS
{
    "original_name": None,
    "parsed_name": None,
    "website": None,
    "contact": None,
    "about": None,
    "modified": None,
    "orcid_id": None,
}
"""


#TODO test
def map_to_dict(query_tuple):
    mapping = generate_empty_mapping()
    # is set later
    mapping["local_url"] = query_tuple[0]
    mapping["publication"]["date_added"] = query_tuple[1].year
    authors_list = split_authors(query_tuple[2])
    for author in authors_list:
        stripped_numbers = re.sub(r'\d{4}', '', author).strip()
        author_dict = {
            "original_name": author,
            "parsed_name": stripped_numbers,
            "website": None,
            "contact": None,
            "about": None,
            "modified": None,
            "orcid_id": None,
        }
        mapping["authors"].append(author_dict)

    mapping["publication"]["title"] = query_tuple[3]
    mapping["publication"]["pages"] = query_tuple[4]
    mapping["publication"]["date_published"] = query_tuple[5].year
    mapping["publication"]["volume"] = query_tuple[6]
    mapping["pub_release"]["journal"] = query_tuple[7]
    mapping["publication"]["number"] = query_tuple[8]
    mapping["publication"]["doi"] = query_tuple[9]
    mapping["pub_release"]["booktitle"] = query_tuple[13]
    mapping["pub_release"]["school"] = query_tuple[14]
    mapping["pub_release"]["address"] = query_tuple[15]
    mapping["pub_release"]["publisher"] = query_tuple[16]
    mapping["pub_release"]["isbn"] = query_tuple[17]
    mapping["pub_release"]["series"] = query_tuple[18]
    # no mapping required
    mapping["type"] = query_tuple[19]

    return mapping

