from mysqlWrapper.mariadb import MariaDb
from pub_storage.tables import *
from pub_storage.foreign_keys import *
from pub_storage.constants import *
import configparser

def setup_database():
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    credentials = dict(config["MARIADB"])
    connector = MariaDb(credentials)

    connector.create_db(DATABASE_NAME)
    connector.createTable("cluster", CLUSTER.format("InnoDB"))
    connector.createTable("publication", PUBLICATION.format("InnoDB"))
    connector.createTable("global_url", GLOBAL_URL.format("InnoDB"))
    connector.createTable("local_url", LOCAL_URL.format("InnoDB"))
    connector.add_foreign_key(GLOBAL_URL_LOCAL_URL_FK)

    connector.close_connection()





