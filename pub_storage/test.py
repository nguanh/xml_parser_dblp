from mysqlWrapper.mariadb import MariaDb
from pub_storage.setup_database import setup_database
from pub_storage.constants import *
from pub_storage.init_dblp import init_dblp

from pub_storage.helper import normalize_title,parse_authors
import configparser


setup_database()
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

credentials = dict(config["MARIADB"])
read_connector = MariaDb(credentials)
write_connector = MariaDb(credentials)
dblp_data = init_dblp()


# iterate through dblp articles
query = "SELECT * FROM harvester.dblp_article WHERE last_harvested = 0"

read_connector.cursor.execute(query)

for (key, mdate, authors, title, pages, pub_year,
     volume, journal, journal_number, ee, url, cite,
     crossref, booktitle, last_updated, harvested) in read_connector.cursor:

    # insert local url
    insert_local_url = ("INSERT INTO storage.local_url(global_url_id,url) VALUES (%s, %s)")
    write_connector.set_query(insert_local_url)
    write_connector.execute((dblp_data['global_url'], key))
    # store local url id as id of this dataset
    identifier = write_connector.cursor.lastrowid

    # insert cluster name
    normalized_title = normalize_title(title)
    insert_cluster = ("INSERT INTO storage.cluster(cluster_name) VALUES (%s)")
    write_connector.set_query(insert_cluster)
    write_connector.execute((normalized_title,))

    #create new authors group
    insert_author_group = ("INSERT INTO storage.authors_group VALUES ()")
    write_connector.set_query(insert_author_group)
    write_connector.execute(())
    author_group_id = write_connector.cursor.lastrowid

    # insert authors
    authors_list = parse_authors(authors)
    for autor_name in authors_list:
        insert_author = ("INSERT INTO storage.authors(main_name, block_name, modified) "
                         "VALUES (%s, %s, CURRENT_TIMESTAMP)")
        write_connector.set_query(insert_author)
        write_connector.execute((autor_name["real"], autor_name["block"]))
        author_id = write_connector.cursor.lastrowid
        # add alias
        insert_alias = ("INSERT INTO storage.name_alias(authors_id, local_url_id, alias) "
                         "VALUES (%s, %s,%s)")
        write_connector.set_query(insert_alias)
        write_connector.execute((author_id,identifier,autor_name["original"]))
        #add to publication authors
        insert_publication_authors = ("INSERT INTO storage.publication_authors(group_id, author_id)"
                         "VALUES (%s, %s)")
        write_connector.set_query(insert_publication_authors)
        write_connector.execute((author_group_id,author_id))







