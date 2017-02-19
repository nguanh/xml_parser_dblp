from mysqlWrapper.mariadb import MariaDb
from pub_storage.setup_database import setup_database
from pub_storage.constants import *
from pub_storage.init_dblp import init_dblp

from pub_storage.helper import normalize_title,get_name_block, parse_pages
import configparser


setup_database(DATABASE_NAME)
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

credentials = dict(config["MARIADB"])
read_connector = MariaDb(credentials)
write_connector = MariaDb(credentials)
dblp_data = init_dblp()

write_connector.connector.database = DATABASE_NAME

# iterate through dblp articles
query = "SELECT * FROM harvester.dblp_article WHERE last_harvested = 0"

read_connector.cursor.execute(query)

for (key, mdate, authors, title, pages, pub_year,
     volume, journal, journal_number, ee, url, cite,
     crossref, booktitle, last_updated, harvested) in read_connector.cursor:

    # insert local url
    insert_local_url = "INSERT INTO local_url(global_url_id,url) VALUES (%s, %s)"
    write_connector.set_query(insert_local_url)
    write_connector.execute((dblp_data['global_url'], key))
    # store local url id as id of this dataset
    identifier = write_connector.cursor.lastrowid

    # insert cluster name
    normalized_title = normalize_title(title)
    insert_cluster = "INSERT INTO cluster(cluster_name) VALUES (%s)"
    write_connector.set_query(insert_cluster)
    write_connector.execute((normalized_title,))

    # insert authors
    authors_list = get_name_block(authors)
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







