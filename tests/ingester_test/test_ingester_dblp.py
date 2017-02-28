from unittest import TestCase

from dblp.queries import DBLP_ARTICLE, ADD_DBLP_ARTICLE
from pub_storage.init_dblp import init_dblp
from pub_storage.ingester import ingest_data
from dblp.queries import INGESTION
from dblp.ingestion import map_to_dict

from .ingester_tools import compare_tables, delete_database,setup_tables
import datetime
TESTDB = "ingester_test"

#TODO weitere tabellen hinzufügen
test_success = {
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
    "name_alias": [
        [1,1, "Ian F. Akyildiz"],
        [3,2, "Horst von Brand"],
        [5,3, "Walter Vogler"],
        [7,4, "Christian Stahl"],
        [10,5, "Richard Müller"],
        [9,5, "Richard Müller 0001"],
    ],
    "cluster": [
        [1, "bla bla bla"],
        [2, "kam kim kum"]
    ]
}


class TestIngsterDblp(TestCase):

    def test_success(self):
        setup_tables("dblp_test1.csv", TESTDB, DBLP_ARTICLE, ADD_DBLP_ARTICLE)
        dblp_data = init_dblp(TESTDB)
        self.assertEqual(dblp_data["global_url"], 1)
        ingest_data(dblp_data, INGESTION.format(TESTDB + ".dblp_article"), map_to_dict, TESTDB)
        compare_tables(self, test_success, TESTDB)

    def tearDown(self):
        delete_database(TESTDB)


