from mysqlWrapper.mariadb import MariaDb
from pub_storage.constants import *
import configparser


def init_dblp():
    # 1. iterate through dblp dataset
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    retVal = {}

    credentials = dict(config["MARIADB"])
    connector = MariaDb(credentials)
    #find global url/ add global URL
    global_url_query = "SELECT id FROM storage.global_url WHERE domain = 'http://dblp.uni-trier.de'"
    connector.cursor.execute(global_url_query)
    result = connector.cursor.fetchone()
    if result is None:
        insert_global_url = ("INSERT INTO storage.global_url(domain,url) "
                             "VALUES ('http://dblp.uni-trier.de','http://dblp.uni-trier.de/rec/xml/')")
        connector.set_query(insert_global_url)
        connector.execute(())
        connector.cursor.execute(global_url_query)
        result = connector.cursor.fetchone()

    connector.close_connection()

    #clear results
    retVal["global_url"] = result[0]
    return retVal
