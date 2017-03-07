from mysqlWrapper.mariadb import MariaDb
from pub_storage.tables import *
from pub_storage.foreign_keys import *
from conf.config import get_config


def setup_database(db_name):

    credentials = dict(get_config("MARIADB"))
    connector = MariaDb(credentials)

    storage_engine = get_config("MISC")["storage_engine"]

    # create database
    connector.create_db(db_name)

    # create tables
    connector.createTable("global_url", GLOBAL_URL.format(storage_engine))
    connector.createTable("local_url", LOCAL_URL.format(storage_engine))

    connector.createTable("publication_authors", PUBLICATION_AUTHORS.format(storage_engine))
    connector.createTable("authors", AUTHORS.format(storage_engine))
    connector.createTable("name_alias", NAMEALIAS.format(storage_engine))
    connector.createTable("alias_source", ALIASSOURCE.format(storage_engine))

    connector.createTable("cluster", CLUSTER.format(storage_engine))
    connector.createTable("publication", PUBLICATION.format(storage_engine))

    # create foreign keys
    connector.add_foreign_key(LOCAL_URL_FK)
    connector.add_foreign_key(PUBLICATIONS_AUTHORS_FK)
    connector.add_foreign_key(NAME_ALIAS_FK)
    connector.add_foreign_key(ALIAS_SOURCE_FK)
    connector.add_foreign_key(PUBLICATION_FK)

    # insert default
    global_url =("INSERT INTO global_url(id,domain,url) "
                 "VALUES (1,'http://localhost/publications','http://localhost/publications'),"
                 "       (2,'http://localhost/users','http://localhost/users')"
                 "ON DUPLICATE KEY UPDATE domain= VALUES(domain),"
                 "                        url   = VALUES(url)")

    connector.execute_ex(global_url)
    connector.close_connection()








