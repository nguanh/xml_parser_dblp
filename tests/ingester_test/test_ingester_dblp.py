from unittest import TestCase
from pub_storage.setup_database import setup_database
from mysqlWrapper.mariadb import MariaDb
from dblp.queries import DBLP_ARTICLE,ADD_DBLP_ARTICLE
import csv

from pub_storage.init_dblp import init_dblp
from pub_storage.ingester import ingest_data
from dblp.queries import INGESTION
from dblp.ingestion import map_to_dict

from conf.config import get_config
from .ingester_tools import compare_tables, delete_database
import datetime
TESTDB = "ingester_test"


#TODO weitere tabellen hinzufügen
test_success={
    "local_url": [
        [1, 1, 'journals/acta/AkyildizB89', datetime.datetime(1990, 1, 1, 1, 1, 1)],
        [2, 1, 'journals/acta/VoglerS014', datetime.datetime(1990, 1, 1, 1, 1, 1)],
    ],
    "authors": [
        [1, "Ian F. Akyildiz", "akyildiz,i", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None],
        [2, "Horst von Brand", "von brand,h", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None],
        [3, "Walter Vogler", "vogler,w", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None],
        [4, "Christian Stahl", "stahl,c", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None],
        [5, "Richard Müller", "muller,r", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None]
    ],
    "cluster":[
        [1,"bla bla bla"],
        [2,"kam kim kum"]

    ]
}


class TestIngsterDblp(TestCase):
    def setUp(self):
        # load testconfig
        credentials = dict(get_config("MARIADB"))
        # setup database
        connector = MariaDb(credentials)
        connector.create_db(TESTDB)
        connector.connector.database = TESTDB
        connector.createTable("test dblp table", DBLP_ARTICLE)

        # setup test ingester database
        setup_database(TESTDB, path="test.ini")
        # import records from csv
        with open('dblp_test1.csv', newline='', encoding='utf-8') as csvfile:
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
        connector.close_connection()

    def test_success(self):
        dblp_data = init_dblp(TESTDB)
        self.assertEqual(dblp_data["global_url"], 1)
        ingest_data(dblp_data, INGESTION.format(TESTDB + ".dblp_article"), map_to_dict, TESTDB)
        compare_tables(self, test_success, TESTDB)

    def tearDown(self):
        delete_database(TESTDB)


