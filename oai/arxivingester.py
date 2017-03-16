from pub_storage.Iingester import Iingester
from mysqlWrapper.mariadb import MariaDb
from conf.config import get_config
from pub_storage.helper import split_authors
import re

def is_not_empty(var):
    return var is not None and len(var) > 0

class DblpIngester(Iingester):
    def __init__(self, ingester_db, harvester_db):
        credentials = dict(get_config("MARIADB"))
        connector = MariaDb(credentials)
        connector.connector.database = ingester_db
        # find global url/ add global URL
        global_url_query = "SELECT id FROM global_url WHERE domain = 'http://arxiv.org'"
        result = connector.fetch_one((), global_url_query)
        if result is None:
            insert_global_url = ("INSERT INTO global_url(domain,url) "
                                 "VALUES ('http://arxiv.org','http://arxiv.org/abs/')")
            connector.execute_ex(insert_global_url)
            result = connector.fetch_one((), global_url_query)
        connector.close_connection()
        self.global_url = result
        self.harvester_db = harvester_db
        pass

    def get_query(self):
        return "SELECT * FROM {}.arxiv_articles WHERE last_harvested = 0".format(self.harvester_db)

    def get_global_url(self):
        return self.global_url

    def update_harvested(self):
        pass

    def get_name(self):
        return "ingester.arxiv"

    def mapping_function(self, query_tuple):
        mapping = self.generate_empty_mapping()
        # is set later
        mapping["local_url"] = query_tuple[0]
        mapping["publication"]["date_published"] = query_tuple[1].year #TODO parse date
        mapping["publication"]["date_added"] = query_tuple[13].year #TODO parse date
        authors_list = split_authors(query_tuple[3])
        for author in authors_list:
            stripped_numbers = re.sub(r'\d{4}', '', author).strip()
            mapping["authors"].append(self.generate_author_mapping(author,stripped_numbers))

        mapping["publication"]["title"] = query_tuple[4]
        mapping["publication"]["abstract"] = query_tuple[10]
        mapping["publication"]["doi"] = query_tuple[12]
        mapping["study_fields"] = query_tuple[11]
        mapping["publication"]["volume"] = query_tuple[6]
        mapping["pub_release"]["journal"] = query_tuple[7]
        mapping["publication"]["number"] = query_tuple[8]
        mapping["publication"]["doi"] = query_tuple[9]
        mapping["publication"]["type_ids"] = 1

        #TODO try to extract some information from journalref
        return mapping
