from unittest import TestCase

from pub_storage.setup_database import setup_database
from pub_storage.ingester import match_author


from .ingester_tools import TESTDB,delete_database, insert_data
from pub_storage.helper import *


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


