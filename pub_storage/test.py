from mysqlWrapper.mariadb import MariaDb
from pub_storage.setup_database import setup_database
from pub_storage.constants import *
from pub_storage.init_dblp import init_dblp
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
    insert_local_url = ("INSERT INTO storage.local_url(global_url_id,url) VALUES (%s, %s)")
    write_connector.set_query(insert_local_url)
    write_connector.execute((dblp_data['global_url'], key))
    print(authors)
    # 2. get authors name
    # 3. generate cluster name
    # 4. generate url
    # 5. add author



def parse_authors(authors_list):
    pass
    #1. autoren nach ; aufsplitten
    #2. (DBLP) zahlen entfernen und zahlen namen und echten namen speichern
    #3. Nachname extrahieren
    #4. Vornamen extrahieren
    #5. alle aliases aus vornamen generieren. z.b Andreas Peter Wendt = A. P. Wendt , A. Wendt, Andreas P. Wendt usw
    #6. normalisieren