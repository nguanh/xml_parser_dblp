from mysqlWrapper.mariadb import MariaDb
from pub_storage.tables import *
from pub_storage.foreign_keys import *
from pub_storage.constants import *
import configparser


def setup_database(db_name):
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    credentials = dict(config["MARIADB"])
    connector = MariaDb(credentials)

    storage_engine = config["MISC"]["storage_engine"]

    # create database
    connector.create_db(db_name)

    # create tables
    connector.createTable("cluster", CLUSTER.format(storage_engine))
    connector.createTable("publication", PUBLICATION.format(storage_engine))
    connector.createTable("global_url", GLOBAL_URL.format(storage_engine))
    connector.createTable("local_url", LOCAL_URL.format(storage_engine))
    connector.createTable("authors", AUTHORS.format(storage_engine))
    connector.createTable("name_alias", NAMEALIAS.format(storage_engine))
    connector.createTable("alias_source", ALIASSOURCE.format(storage_engine))
    connector.createTable("publication_authors", PUBLICATION_AUTHORS.format(storage_engine))
    connector.createTable("default table", DEFAULT_TABLE.format(storage_engine))
    connector.createTable("difference table", DIFFERENCE_TABLE.format(storage_engine))

    # create foreign keys
    connector.add_foreign_key(LOCAL_URL_FK)
    connector.add_foreign_key(NAME_ALIAS_FK)
    connector.add_foreign_key(ALIAS_SOURCE_FK)
    connector.add_foreign_key(PUBLICATIONS_AUTHORS_FK)
    connector.add_foreign_key(DEFAULT_TABLE_FK)

    connector.close_connection()








