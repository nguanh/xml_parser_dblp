from mysqlWrapper.mariadb import MariaDb
from pub_storage.setup_database import setup_database
from pub_storage.constants import *
from pub_storage.init_dblp import init_dblp
from pub_storage.queries import *

from dblp.queries import INGESTION
from dblp.ingestion import map_to_dict

from pub_storage.helper import normalize_title, parse_authors, parse_pages
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
    write_connector.cursor.execute(CHECK_LOCAL_URL, (mapping["local_url"], dblp_data['global_url']))
    duplicate_id = write_connector.cursor.fetchone()
    if duplicate_id is not None:
        #TODO duplicate skip
        print("Skipping duplicate", mapping["local_url"])
        continue
    # insert local url
    write_connector.set_query(INSERT_LOCAL_URL)
    identifier = write_connector.execute((mapping["local_url"], dblp_data['global_url']))

    # ------------------------- CLUSTER --------------------------------------------------------------------------------
    cluster_name = normalize_title(mapping["publication"]["title"])
    # check for matching cluster (so far ONLY COMPLETE MATCH) TODO levenshtein distance
    write_connector.cursor.execute(CHECK_CLUSTER, (cluster_name,))
    cluster_matches =[]
    for match in write_connector.cursor:
        cluster_matches.append(match[0])

    if len(cluster_matches) == 0:
        print("Creating new Cluster")
        write_connector.set_query(INSERT_CLUSTER)
        write_connector.execute((cluster_name,))

    elif len(cluster_matches) == 1:
        print("Appending cluster")
        #TODO
    else:
        print("ambiguous matches, move dataset to other database  ")
        #TODO

    '''
    # insert authors
    authors_list = parse_authors(authors)
    for autor_name in authors_list:
        insert_author = ("INSERT INTO authors(main_name, block_name, modified) "
                         "VALUES (%s, %s, CURRENT_TIMESTAMP)")
        write_connector.set_query(insert_author)
        write_connector.execute((autor_name["real"], autor_name["block"]))
        author_id = write_connector.cursor.lastrowid
        # add alias
        insert_alias = ("INSERT INTO name_alias(authors_id, local_url_id, alias) "
                        "VALUES (%s, %s,%s)")
        write_connector.set_query(insert_alias)
        write_connector.execute((author_id,identifier,autor_name["original"]))
        # add to publication authors
        insert_publication_authors = ("INSERT INTO publication_authors(url_id, author_id)"
                                      "VALUES (%s, %s)")
        write_connector.set_query(insert_publication_authors)
        write_connector.execute((identifier, author_id))
    page_from, page_to = parse_pages(pages)

    # store rest in default table

    insert_default_table = ("INSERT INTO default_table"
                            "(url_id, title,pages_from,pages_to,journal, number,"
                            " volume,date_published,doi,book_title)"
                                      "VALUES (%s, %s,%s, %s,%s,%s,%s,%s,%s,%s)")
    write_connector.set_query(insert_default_table)
    write_connector.execute((identifier,title,page_from,page_to,journal,journal_number,volume,pub_year.year,ee,booktitle))
    '''
read_connector.close_connection()







