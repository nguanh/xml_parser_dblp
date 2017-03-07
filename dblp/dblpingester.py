from pub_storage.Iingester import Iingester
from mysqlWrapper.mariadb import MariaDb
from conf.config import get_config
from pub_storage.helper import split_authors
import re


class DblpIngester(Iingester):
    def __init__(self, ingester_db, harvester_db):
        credentials = dict(get_config("MARIADB"))
        connector = MariaDb(credentials)
        connector.connector.database = ingester_db
        # find global url/ add global URL
        global_url_query = "SELECT id FROM global_url WHERE domain = 'http://dblp.uni-trier.de'"
        result = connector.fetch_one((), global_url_query)
        if result is None:
            insert_global_url = ("INSERT INTO global_url(domain,url) "
                                 "VALUES ('http://dblp.uni-trier.de','http://dblp.uni-trier.de/rec/xml/')")
            connector.execute_ex(insert_global_url)
            result = connector.fetch_one((), global_url_query)
        connector.close_connection()
        self.global_url = result
        self.harvester_db = harvester_db
        pass

    def get_query(self):
        return ("SELECT * FROM {}.dblp_article WHERE last_harvested = 0").format(self.harvester_db)

    def get_global_url(self):
        return self.global_url

    def update_harvested(self):
        pass

    def mapping_function(self, query_tuple):
        mapping = self.generate_empty_mapping()
        # is set later
        mapping["local_url"] = query_tuple[0]
        mapping["publication"]["date_added"] = query_tuple[1].year
        authors_list = split_authors(query_tuple[2])
        for author in authors_list:
            stripped_numbers = re.sub(r'\d{4}', '', author).strip()
            mapping["authors"].append(self.generate_author_mapping(author,stripped_numbers))

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
