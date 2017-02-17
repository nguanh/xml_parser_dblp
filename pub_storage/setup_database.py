from mysqlWrapper.mariadb import MariaDb
from pub_storage.tables import *
from pub_storage.foreign_keys import *
import configparser
CONFIG_PATH = "../storage.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

credentials = dict(config["MARIADB"])
connector = MariaDb(credentials)
con = MariaDb(credentials)

connector.create_db(DATABASE_NAME)
connector.createTable("cluster", CLUSTER.format("InnoDB"))
connector.createTable("publication", PUBLICATION.format("InnoDB"))
connector.createTable("global_url", GLOBAL_URL.format("InnoDB"))
connector.createTable("local_url", LOCAL_URL.format("InnoDB"))
connector.add_foreign_key(GLOBAL_URL_LOCAL_URL_FK)



#1. iterate through dblp dataset

#find global url/ add global URL
global_url_id = "SELECT id FROM storage.global_url WHERE domain = 'http://dblp.uni-trier.de'"
connector.cursor.execute(global_url_id)
result = connector.cursor.fetchone()
if result is None:
    insert_global_url = ("INSERT INTO storage.global_url(domain,url) "
         "VALUES ('http://dblp.uni-trier.de','http://dblp.uni-trier.de/rec/xml/')")
    connector.set_query(insert_global_url)
    connector.execute(())
    result = connector.cursor.fetchone()

#clear results
#connector.cursor.fetchall()
global_url = result[0]

print(global_url)




# iterate through dblp articles
query = "SELECT * FROM harvester.dblp_article WHERE last_harvested = 0"

connector.cursor.execute(query)

#warum wird nur eine iteration durchlaufen?
for (key, mdate, authors, title, pages, pub_year,
     volume, journal, journal_number, ee, url, cite,
     crossref, booktitle, last_updated, harvested) in connector.cursor:
    insert_local_url = ("INSERT INTO storage.local_url(global_url_id,url) VALUES (%s, %s)")
    con.set_query(insert_local_url)
    con.execute((global_url,key))
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