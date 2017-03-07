from unittest import TestCase

from dblp.queries import DBLP_ARTICLE, ADD_DBLP_ARTICLE
from pub_storage.init_dblp import init_dblp
from pub_storage.ingester import ingest_data2
from dblp.queries import INGESTION
from dblp.ingestion import map_to_dict
from pub_storage.setup_database import setup_database
from .ingester_tools import compare_tables, delete_database,setup_tables,TESTDB,insert_data
import datetime


#TODO weitere tabellen hinzufügen
test_success = {
    "local_url": {
        (1, 3, None, None, None, 'journals/acta/AkyildizB89', datetime.datetime(1990, 1, 1, 1, 1, 1)),
        (2, 1, None, None, None, 'TODO PLATZHALTER', datetime.datetime(1990, 1, 1, 1, 1, 1)),
        (3, 3, None, None, None, 'journals/acta/VoglerS014', datetime.datetime(1990, 1, 1, 1, 1, 1)),
        (4, 1, None, None, None, 'TODO PLATZHALTER', datetime.datetime(1990, 1, 1, 1, 1, 1)),
    },
    "authors": {
        (1, "Ian F. Akyildiz", "akyildiz,i", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (2, "Horst von Brand", "von brand,h", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (3, "Walter Vogler", "vogler,w", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (4, "Christian Stahl", "stahl,c", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (5, "Richard Müller", "muller,r", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None)
    },
    "name_alias": {
        (1, 1, "Ian F. Akyildiz"),
        (3, 2, "Horst von Brand"),
        (5, 3, "Walter Vogler"),
        (7, 4, "Christian Stahl"),
        (9, 5, "Richard Müller 0001"),
        (10, 5, "Richard Müller"),
    },
    "cluster": {
        (1, "bla bla bla"),
        (2, "kam kim kum")
    },

    "alias_source": {
        (1, 1, 1),
        (3, 1, 3),
        (5, 3, 5),
        (7, 3, 7),
        (9, 3, 9),
        (10, 3, 10),
    },

    "publication_authors": {
        (1, 1, 1, 0),
        (2, 1, 2, 1),
        (3, 2, 1, 0),
        (4, 2, 2, 1),
        (5, 3, 3, 0),
        (6, 3, 4, 1),
        (7, 3, 5, 2),
        (8, 4, 3, 0),
        (9, 4, 4, 1),
        (10, 4, 5, 2),
    },

}
"""
    "publication": {
        (1, 2, 1, None, "Bla Bla Bla", "1-5", None, "dummydoi", None, None, "2011", "1989", "1", "2"),
        (2, 4, 2, None, "Kam? Kim! Kum.", "10-11", None, "doidoi", None, None, "2014", "2014", "51", "8")
    },

"""



class TestIngsterDblp(TestCase):

    def test_success(self):
        setup_tables("dblp_test1.csv", DBLP_ARTICLE, ADD_DBLP_ARTICLE)
        dblp_data = init_dblp(TESTDB)
        self.assertEqual(dblp_data["global_url"], 3)
        ingest_data2(dblp_data, INGESTION.format(TESTDB + ".dblp_article"), map_to_dict, TESTDB)
        compare_tables(self, test_success, ignore_id=True)

    def test_setup_database(self):
        setup_database(TESTDB)
        setup_database(TESTDB)

    def tearDown(self):
        delete_database(TESTDB)
        pass


