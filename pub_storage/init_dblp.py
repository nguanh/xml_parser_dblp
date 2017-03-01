from mysqlWrapper.mariadb import MariaDb
from conf.config import get_config


def init_dblp(database = "storage"):
    # 1. iterate through dblp dataset
    retVal = {}

    credentials = dict(get_config("MARIADB"))
    connector = MariaDb(credentials)
    connector.connector.database = database
    # find global url/ add global URL
    global_url_query = "SELECT id FROM global_url WHERE domain = 'http://dblp.uni-trier.de'"
    result = connector.fetch_one((), global_url_query)
    if result is None:

        insert_global_url = ("INSERT INTO global_url(domain,url) "
                             "VALUES ('http://dblp.uni-trier.de','http://dblp.uni-trier.de/rec/xml/')")
        connector.execute_ex(insert_global_url)
        result = connector.fetch_one((), global_url_query)

    connector.close_connection()

    retVal["global_url"] = result
    return retVal
