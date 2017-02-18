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
print(dblp_data)

# iterate through dblp articles
query = "SELECT * FROM harvester.dblp_article WHERE last_harvested = 0"

read_connector.cursor.execute(query)

#warum wird nur eine iteration durchlaufen?
for (key, mdate, authors, title, pages, pub_year,
     volume, journal, journal_number, ee, url, cite,
     crossref, booktitle, last_updated, harvested) in read_connector.cursor:
    # insert local url
    insert_local_url = ("INSERT INTO storage.local_url(global_url_id,url) VALUES (%s, %s)")
    write_connector.set_query(insert_local_url)
    write_connector.execute((dblp_data['global_url'], key))

    # insert cluster name
    normalized_title = normalize_title(title)
    insert_cluster = ("INSERT INTO storage.cluster(cluster_name) VALUES (%s)")
    write_connector.set_query(insert_cluster)
    write_connector.execute((normalized_title,))
    parse_authors(authors)
    # 2. get authors name
    # 3. generate cluster name
    # 4. generate url
    # 5. add author


