from unittest import TestCase
from pub_storage.setup_database import setup_database
from mysqlWrapper.mariadb import MariaDb
from dblp.queries import DBLP_ARTICLE
import configparser
from .queries import IMPORT_CSV

from mysql.connector.constants import ClientFlag

TESTDB = "ingester_test"


class TestIngsterDblp(TestCase):
    @classmethod
    def setUpClass(cls):
        # load testconfig
        config = configparser.ConfigParser()
        config.read("test.ini")
        print(ClientFlag.LOCAL_FILES)
        credentials = dict(config["MARIADB"])
        credentials["client_flags"] = ClientFlag.LOCAL_FILES
        print(credentials)
        # setup database
        connector = MariaDb(credentials)
        connector.create_db(TESTDB)
        connector.connector.database = TESTDB
        connector.createTable("test dblp table", DBLP_ARTICLE)
        print(IMPORT_CSV.format("test.ini", "dblp_article"))
        connector.execute_ex(IMPORT_CSV.format("test.ini", "dblp_article"))
        # setup test ingester database
        setup_database(TESTDB, path="test.ini")
        # import records from csv


    def testest(self):
        print("hi")

