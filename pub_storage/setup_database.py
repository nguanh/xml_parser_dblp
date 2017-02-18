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

    # create database
    connector.create_db(DATABASE_NAME)

    # create tables
    connector.createTable("cluster", CLUSTER.format("InnoDB"))
    connector.createTable("publication", PUBLICATION.format("InnoDB"))
    connector.createTable("global_url", GLOBAL_URL.format("InnoDB"))
    connector.createTable("local_url", LOCAL_URL.format("InnoDB"))
    connector.createTable("authors", AUTHORS.format("InnoDB"))
    connector.createTable("name_alias", NAMEALIAS.format("InnoDB"))
    connector.createTable("publication_authors", PUBLICATION_AUTHORS.format("InnoDB"))

    # create foreign keys
    connector.add_foreign_key(LOCAL_URL_FK)
    connector.add_foreign_key(NAME_ALIAS_FK)
    connector.add_foreign_key(PUBLICATIONS_AUTHORS_FK)

    connector.close_connection()








