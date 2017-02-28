from mysqlWrapper.mariadb import MariaDb
from conf.config import get_config

def init_dblp(database = "storage"):
    # 1. iterate through dblp dataset
    retVal = {}

    credentials = dict(get_config("MARIADB"))
    connector = MariaDb(credentials)
    connector.connector.database = database
    #find global url/ add global URL
    global_url_query = "SELECT id FROM global_url WHERE domain = 'http://dblp.uni-trier.de'"
    connector.cursor.execute(global_url_query)
    result = connector.cursor.fetchone()
    if result is None:

        insert_global_url = ("INSERT INTO global_url(domain,url) "
                             "VALUES ('http://dblp.uni-trier.de','http://dblp.uni-trier.de/rec/xml/')")
        connector.set_query(insert_global_url)
        connector.execute(())
        connector.cursor.execute(global_url_query)
        result = connector.cursor.fetchone()

    connector.close_connection()

    #clear results
    retVal["global_url"] = result[0]
    return retVal
