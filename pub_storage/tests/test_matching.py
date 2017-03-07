from unittest import TestCase

from pub_storage.setup_database import setup_database
from pub_storage.ingester import match_author, match_title


from .ingester_tools import TESTDB, delete_database, insert_data
from pub_storage.helper import *


class TestMatchTitle(TestCase):

    def test_success_empty_db(self):
        # setup empty testdb
        setup_database(TESTDB)
        result = match_title("Single Title", TESTDB)
        self.assertEqual(result,{
                "status": Status.SAFE,
                "match": Match.NO_MATCH,
                "id": None,
                "reason": None,
            })

    def test_multi_cluster_match(self):
        setup_database(TESTDB)
        insert_data("INSERT into cluster (id,cluster_name) VALUES(1,'multi title'),(2,'multi title')")
        result = match_title("Multi Title", TESTDB)
        self.assertEqual(result,{
                "status": Status.LIMBO,
                "match": Match.MULTI_MATCH,
                "id": None,
                "reason": Reason.AMB_CLUSTER,
            })

    def test_single_cluster_single_pub(self):
        setup_database(TESTDB)
        insert_data("INSERT into global_url (id,domain,url) VALUES(5,'a','a')")
        insert_data("INSERT into local_url (id,url,global_url_id) VALUES(1,'a',5)")
        insert_data("INSERT into cluster (id,cluster_name) VALUES(1,'multi title'),(2,'single title')")
        insert_data("INSERT into publication(id,url_id,cluster_id, title)VALUES (1,1,2,'hi')")
        result = match_title("single Title", TESTDB)
        self.assertEqual(result,{
                "status": Status.SAFE,
                "match": Match.SINGLE_MATCH,
                "id": 2,
                "reason": None,
            })

    def test_single_cluster_multi_no_pub(self):
        setup_database(TESTDB)
        insert_data("INSERT into global_url (id,domain,url) VALUES(5,'a','a')")
        insert_data("INSERT into local_url (id,url,global_url_id) VALUES(1,'a',5)")
        insert_data("INSERT into cluster (id,cluster_name) VALUES(1,'multi title'),(2,'single title')")
        # no publications for cluster, why so ever
        result = match_title("single Title", TESTDB)
        self.assertEqual(result,{
                "status": Status.LIMBO,
                "match": Match.SINGLE_MATCH,
                "id": None,
                "reason": Reason.AMB_PUB,
            })

    def tearDown(self):
        delete_database(TESTDB)
        pass


class TestMatchAuthors(TestCase):

    def test_success_empty_db(self):
        # setup empty testdb
        setup_database(TESTDB)
        authors=[{
            "original_name": "Karl Bauer",
            "parsed_name": "Karl Bauer",
            "website": None,
            "contact": None,
            "about": None,
            "modified": None,
            "orcid_id": None,
        },
        {
            "original_name": "Jarl Mauer",
            "parsed_name": "Jarl Mauer",
            "website": None,
            "contact": None,
            "about": None,
            "modified": None,
            "orcid_id": None,
        },
        ]
        result = match_author(authors,TESTDB)
        self.assertEqual(result,[{
                "status": Status.SAFE,
                "match": Match.NO_MATCH,
                "id": None,
                "reason": None,
            },
            {
                "status": Status.SAFE,
                "match": Match.NO_MATCH,
                "id": None,
                "reason": None,
            }
        ])

    def test_single_block_match(self):
        setup_database(TESTDB)
        insert_data("INSERT into AUTHORS (id, block_name,main_name) VALUES(5,'gruber,h', 'Hans Gruber')")
        authors = [{
            "original_name": "Hans Meyer Gruber",
            "parsed_name": "Hans Meyer Gruber",
            "website": None,
            "contact": None,
            "about": None,
            "modified": None,
            "orcid_id": None,
        },
        ]
        result = match_author(authors,TESTDB)

        self.assertEqual(result,[{
                "status": Status.SAFE,
                "match": Match.SINGLE_MATCH,
                "id": 5,
                "reason": None,
            },
        ])

    def test_multi_block_alias_match(self):
        setup_database(TESTDB)
        insert_data("INSERT into authors (id, block_name,main_name) "
                    "VALUES(5,'gruber,h', 'Hans Gruber'),(1,'gruber,h', 'Heinrich Gruber')")

        insert_data("INSERT into name_alias (id, authors_id,alias) "
                    "VALUES(1,1, 'Heichrich Gruber'),(2,1, 'Heinrich F. Gruber'),"
                    "(3,5, 'Hans Gruber'),(4,5, 'Hans Meyer Gruber')")
        authors = [{
            "original_name": "Hans Meyer Gruber",
            "parsed_name": "Hans Meyer Gruber",
            "website": None,
            "contact": None,
            "about": None,
            "modified": None,
            "orcid_id": None,
        },
        ]
        result = match_author(authors, TESTDB)

        self.assertEqual(result,[{
                "status": Status.SAFE,
                "match": Match.MULTI_MATCH,
                "id": 5,
                "reason": None,
            },
        ])

    def test_multi_block_alias_no_match(self):
        setup_database(TESTDB)
        insert_data("INSERT into authors (id, block_name,main_name) "
                    "VALUES(5,'gruber,h', 'Hans Gruber'),(1,'gruber,h', 'Heinrich Gruber')")

        insert_data("INSERT into name_alias (id, authors_id,alias) "
                    "VALUES(1,1, 'Heichrich Gruber'),(2,1, 'Heinrich F. Gruber'),"
                    "(3,5, 'Heichrich Gruber'),(4,5, 'Heinrich F. Gruber')")
        authors = [{
            "original_name": "Hans Meyer Gruber",
            "parsed_name": "Hans Meyer Gruber",
            "website": None,
            "contact": None,
            "about": None,
            "modified": None,
            "orcid_id": None,
        },
        ]
        result = match_author(authors, TESTDB)

        self.assertEqual(result, [{
            "status": Status.LIMBO,
            "match": Match.MULTI_MATCH,
            "id": None,
            "reason": Reason.AMB_ALIAS,
        },
        ])


    def tearDown(self):
        delete_database(TESTDB)
        pass


