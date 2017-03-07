from abc import ABC, abstractmethod


class Iingester(ABC):
    def __init__(self, database):
        pass
    @abstractmethod
    def get_query(self):
        pass
    @abstractmethod
    def get_global_url(self):
        pass
    @abstractmethod
    def mapping_function(self, query_dataset):
        pass
    @abstractmethod
    def update_harvested(self):
        pass

    @staticmethod
    def generate_empty_mapping():
        return {
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

    @staticmethod
    def generate_author_mapping(original_name,parsed_name, website = None, contact = None, about = None,
                                modified = None, orcid_id = None):
        return{
            "original_name": original_name,
            "parsed_name": parsed_name,
            "website": website,
            "contact": contact,
            "about": about,
            "modified": modified,
            "orcid_id": orcid_id,
        }