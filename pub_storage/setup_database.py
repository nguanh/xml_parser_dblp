from mysqlWrapper.mariadb import MariaDb
from pub_storage.queries import *
import configparser
CONFIG_PATH = "../storage.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

credentials = dict(config["MARIADB"])
connector = MariaDb(credentials)

connector.create_db(DATABASE_NAME)
connector.createTable(DATABASE_NAME, CLUSTER.format("InnoDB"))
connector.createTable(DATABASE_NAME, PUBLICATION.format("InnoDB"))


#1. iterate through dblp dataset
query = "SELECT * FROM harvester.dblp_article WHERE last_harvested = 0"

connector.cursor.execute(query)

for (key, mdate, authors, title, pages, pub_year,
     volume, journal, journal_number, ee, url, cite,
     crossref, booktitle, last_updated, harvested) in connector.cursor:

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