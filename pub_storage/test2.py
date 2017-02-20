from mysqlWrapper.mariadb import MariaDb
from pub_storage.setup_database import setup_database
from pub_storage.constants import *
from pub_storage.init_dblp import init_dblp
from pub_storage.queries import *

from dblp.queries import INGESTION
from dblp.ingestion import map_to_dict

from pub_storage.helper import normalize_title, get_name_block, parse_pages
import configparser


setup_database(DATABASE_NAME)
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

credentials = dict(config["MARIADB"])
read_connector = MariaDb(credentials)
write_connector = MariaDb(credentials)
dblp_data = init_dblp()

write_connector.connector.database = DATABASE_NAME


read_connector.cursor.execute(INGESTION)

for query_dataset in read_connector.cursor:
    mapping = map_to_dict(query_dataset)

    # ------------------------- LOCAL_URL ------------------------------------------------------------------------------
    # check for duplicates by looking up the local URL
    duplicate_id = write_connector.fetch_one((mapping["local_url"], dblp_data['global_url']),CHECK_LOCAL_URL)
    if duplicate_id is not None:
        #TODO duplicate skip
        print("Skipping duplicate", mapping["local_url"])
        continue
    # insert local url
    identifier = write_connector.execute_ex(INSERT_LOCAL_URL, (mapping["local_url"], dblp_data['global_url']))

    # ------------------------- CLUSTER --------------------------------------------------------------------------------
    cluster_name = normalize_title(mapping["publication"]["title"])
    # check for matching cluster (so far ONLY COMPLETE MATCH) TODO levenshtein distance
    write_connector.cursor.execute(CHECK_CLUSTER, (cluster_name,))
    cluster_matches = []
    for match in write_connector.cursor:
        cluster_matches.append(match[0])

    if len(cluster_matches) == 0:
        print("Creating new Cluster")
        write_connector.execute_ex(INSERT_CLUSTER, (cluster_name,))

    elif len(cluster_matches) == 1:
        print("Appending cluster")
        #TODO
    else:
        print("ambiguous matches, move dataset to other database  ")
        #TODO

    # ------------------------- AUTHORS --------------------------------------------------------------------------------
    for author_dict in mapping["authors"]:
        name_block = get_name_block(author_dict["parsed_name"])
        # find matching existing author with name block
        author_block_match = write_connector.fetch_one((name_block,), COUNT_AUTHORS)
        # case 0 matching name blocks: create new  publication author
        # TODO handle None
        # TODO durch dict ersetzen die query
        if author_block_match == 0:
            author_dict["block_name"] = name_block
            author_id = write_connector.execute_ex(INSERT_AUTHORS, author_dict)
            # add original name as alias
            write_connector.execute_ex(INSERT_ALIAS, (author_id, author_dict["original_name"]))
            write_connector.execute_ex(SELECT_ALIAS, (author_id, author_dict["original_name"]))
            write_connector.execute_ex(INSERT_ALIAS_SOURCE, (identifier,))
            # add parsed name as alias, if it's = original name, skip
            write_connector.execute_ex(INSERT_ALIAS, (author_id, author_dict["parsed_name"]))
            write_connector.execute_ex(SELECT_ALIAS, (author_id, author_dict["parsed_name"]))
            write_connector.execute_ex(INSERT_ALIAS_SOURCE, (identifier,))
            # add to publication authors
            write_connector.execute_ex(INSERT_PUBLICATION_AUTHORS, (identifier, author_id))

        # case 1 matching name blocks: include author names as possible alias
        elif author_block_match == 1:
            pass
        # case more than 1 matching name blocks: create new block TODO match by alias ?
        else:
            pass

    # ------------------------- DEFAULT/DIFFERENCE TABLE ---------------------------------------------------------------
    mapping['publication']['url_id'] = identifier
    # new cluster, insert into default table
    if len(cluster_matches) == 0:
        write_connector.execute_ex(INSERT_DEFAULT_TABLE, mapping["publication"])
    else:
        #TODO
        pass

write_connector.close_connection()
read_connector.close_connection()







