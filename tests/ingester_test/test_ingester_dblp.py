from unittest import TestCase

from dblp.queries import DBLP_ARTICLE, ADD_DBLP_ARTICLE
from pub_storage.init_dblp import init_dblp
from pub_storage.ingester import ingest_data
from dblp.queries import INGESTION
from dblp.ingestion import map_to_dict

from .ingester_tools import compare_tables, delete_database,setup_tables,TESTDB,insert_data
import datetime


#TODO weitere tabellen hinzufügen
test_success = {
    "local_url": {
        (1, 1, None, None, None, 'journals/acta/AkyildizB89', datetime.datetime(1990, 1, 1, 1, 1, 1)),
        (2, 1, None, None, None, 'journals/acta/VoglerS014', datetime.datetime(1990, 1, 1, 1, 1, 1)),
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
    "alias_source": {
        (1, 1, 1),
        (3, 1, 3),
        (5, 2, 5),
        (7, 2, 7),
        (9, 2, 9),
        (10, 2, 10),
    },
    "cluster": {
        (1, "bla bla bla"),
        (2, "kam kim kum")
    },
    "publication": {
        (1, 1, 1, None, "Bla Bla Bla", 1, 5, None, "dummydoi", None, None, "2011", "1989", "1", "2"),
        (2, 2, 2, None, "Kam? Kim! Kum.", 10, 11, None, "doidoi", None, None, "2014", "2014", "51", "8")
    },
    "publication_authors": {
        (1, 1, 1, 0),
        (2, 1, 2, 1),
        (3, 2, 3, 0),
        (4, 2, 4, 1),
        (5, 2, 5, 2),
    }

}


test_same_authors = {

    "authors": {
        (1, "Ian F. Akyildiz", "akyildiz,i", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (2, "Horst von Brand", "von brand,h", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (3, "Richard Müller", "muller,r", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None)
    },

    "name_alias": {
        (1, 1, "Ian F. Akyildiz"),
        (5, 1, "Ian Fanning Akyildiz"),
        (7, 2, "Horst K. von Brand"),
        (3, 2, "Horst von Brand"),
        (10, 3, "Richard Müller"),
        (9, 3, "Richard Müller 0001"),
    },
    "alias_source": {
        (1, 1, 1),
        (3, 1, 3),
        (5, 2, 5),
        (7, 2, 7),
        (9, 2, 9),
        (10, 2, 10),
    },
    "cluster": {
        (1, "bla bla bla"),
        (2, "kam kim kum")
    },
    "publication": {
        (1,1,1, None,"Bla Bla Bla",1,5,None,"dummydoi",None,None,"2011","1989","1","2"),
        (2,2,2, None,"Kam? Kim! Kum.",10,11,None,"doidoi",None,None,"2014","2014","51","8")
    },
    "publication_authors": {
        (1,1,1,0),
        (2,1,2,1),
        (3,2,1,0),
        (4,2,2,1),
        (5,2,3,2),
    }
}


test_same_name_block = {

    "authors": {
        (1, "Ina Raus", "raus,i", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (2, "Ian F. Raus", "raus,i", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (3, "Horst von Brand", "von brand,h", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
        (4, "Richard Müller", "muller,r", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None)
    },

    "name_alias": {
        (1, 1, "Ina Raus"),
        (2, 2, "Ian F. Raus"),
        (5, 3, "Horst von Brand"),
        (10, 4, "Richard Müller"),
        (9, 4, "Richard Müller 0001"),
    },

    "alias_source": {
        (1, 1, 2),
        (3, 1, 5),
        (5, 2, 1),
        (7, 2, 9),
        (8, 2, 10),
    },

    "cluster": {
        (1, "bla bla bla"),
        (2, "kam kim kum")
    },
    "publication": {
        (1, 1, 1, None, "Bla Bla Bla", 1, 5, None, "dummydoi", None, None, "2011", "1989", "1", "2"),
        (2, 2, 2, None, "Kam? Kim! Kum.", 10, 11, None, "doidoi", None, None, "2014", "2014", "51", "8")
    },

    "publication_authors": {
        (1, 1, 2, 0),
        (2, 1, 3, 1),
        (3, 2, 1, 0),
        (4, 2, 4, 1),
    }



}


class TestIngsterDblp(TestCase):

    def test_success(self):
        setup_tables("dblp_test1.csv", DBLP_ARTICLE, ADD_DBLP_ARTICLE)
        dblp_data = init_dblp(TESTDB)
        self.assertEqual(dblp_data["global_url"], 1)
        ingest_data(dblp_data, INGESTION.format(TESTDB + ".dblp_article"), map_to_dict, TESTDB)
        compare_tables(self, test_success, ignore_id=True)

    def test_same_authors(self):
        # both publications share 2 common authors, with different style of writing the name
        setup_tables("dblp_test2.csv", DBLP_ARTICLE, ADD_DBLP_ARTICLE)
        dblp_data = init_dblp(TESTDB)
        ingest_data(dblp_data, INGESTION.format(TESTDB + ".dblp_article"), map_to_dict, TESTDB)
        compare_tables(self, test_same_authors, ignore_id= True)

    def test_same_name_block(self):
        # both publications have different authors with same nameblock raus,i
        # usually the system would put both publications into the same block, but for testing purposes
        # we manually create a second author name block
        setup_tables("dblp_test3.csv", DBLP_ARTICLE, ADD_DBLP_ARTICLE)
        dblp_data = init_dblp(TESTDB)
        #create authors
        authors = "INSERT INTO authors (id,main_name,block_name) VALUES(1,'Ina Raus', 'raus,i'),(2,'Ian F. Raus', 'raus,i')"
        insert_data(authors)
        alias = "INSERT INTO name_alias (id,authors_id,alias) VALUES(1,1,'Ina Raus'),(2,2,'Ian F. Raus' )"
        insert_data(alias)
        ingest_data(dblp_data, INGESTION.format(TESTDB + ".dblp_article"), map_to_dict, TESTDB)
        compare_tables(self, test_same_name_block, ignore_id= True)

    def tearDown(self):
        delete_database(TESTDB)
        pass


