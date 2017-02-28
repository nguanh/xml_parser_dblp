from unittest import TestCase
from pub_storage.setup_database import setup_database
from mysqlWrapper.mariadb import MariaDb
from dblp.queries import DBLP_ARTICLE,ADD_DBLP_ARTICLE
import configparser
from .queries import IMPORT_CSV
import csv

from mysql.connector.constants import ClientFlag

TESTDB = "ingester_test"


class TestIngsterDblp(TestCase):
    @classmethod
    def setUpClass(cls):
        # load testconfig
        config = configparser.ConfigParser()
        config.read("test.ini")
        credentials = dict(config["MARIADB"])
        # setup database
        connector = MariaDb(credentials)
        connector.create_db(TESTDB)
        connector.connector.database = TESTDB
        connector.createTable("test dblp table", DBLP_ARTICLE)

        with open('dblp_test1.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            do_once = False
            for row in spamreader:
                # remove last updated and harvest date
                del row[-2:]
                # skip first line
                if do_once is True:
                    tup = tuple(map(lambda x: x if x != "" else None, row))
                    connector.execute_ex(ADD_DBLP_ARTICLE, tup)
                else:
                    do_once = True

        # setup test ingester database
        setup_database(TESTDB, path="test.ini")
        # import records from csv


    def testest(self):
        print("hi")

