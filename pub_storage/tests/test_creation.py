from unittest import TestCase

from pub_storage.setup_database import setup_database
from pub_storage.ingester import create_authors, create_title, create_publication, update_diff_tree
from .ingester_tools import TESTDB, delete_database, insert_data, compare_tables, get_pub_dict
from pub_storage.helper import *
from pub_storage.difference_storage import *
import datetime


class TestUpdateDiffTree(TestCase):

    def test_no_diff_tree(self):
        setup_database(TESTDB)
        insert_data("INSERT INTO publication(id,url_id,cluster_id) VALUES (5,5,1)")
        # every table is empty
        pub_dict = get_pub_dict(url_id=1, title="Hello World", date_published=datetime.datetime(1990,1,1,1,1,1))
        author_ids=[1,4,7]
        result = update_diff_tree(5,pub_dict,author_ids,database=TESTDB)
        self.assertEqual(result["author_ids"],[
            {"value": 1, "votes": 0, "bitvector": 1},
            {"value": 4, "votes": 0, "bitvector": 1},
            {"value": 7, "votes": 0, "bitvector": 1}
        ])

    def test_existing_diff_tree(self):
        setup_database(TESTDB)
        pub_dict = get_pub_dict(url_id=1, title="Hello World Again", date_published=datetime.datetime(1990, 1, 1, 1, 1, 1), author_ids=5)
        diff_tree = generate_diff_store(pub_dict)
        serialized_tree = serialize_diff_store(diff_tree)
        insert_data("INSERT INTO publication(id,url_id,cluster_id, differences) "
                    "VALUES (5,5,1,%s)",(serialized_tree,))
        author_ids=[1,4,7]
        pub_dict = get_pub_dict(url_id=2, title="Hello World", date_published=datetime.datetime(1990, 1, 1, 1, 1, 1))
        result = update_diff_tree(5,pub_dict,author_ids,database=TESTDB)

        self.assertEqual(result["author_ids"],[
            {"value": 5, "votes": 0, "bitvector": 1},
            {"value": 1, "votes": 0, "bitvector": 2},
            {"value": 4, "votes": 0, "bitvector": 2},
            {"value": 7, "votes": 0, "bitvector": 2}
        ])

    def tearDown(self):
        delete_database(TESTDB)


class TestCreatePublication(TestCase):
    def test_no_publication(self):
        setup_database(TESTDB)
        insert_data("INSERT INTO cluster (id,cluster_name) VALUES(1,'random Title')")
        insert_data("INSERT into authors (id,main_name,block_name)"
                    "VALUES(1,'Nina Nonsense','nonsense,n'),(2,'Otto Otter','otter,o')")
        test_success = {
            "local_url": {
                (1,1,None,None,None, "TODO PLATZHALTER",datetime.datetime(1990,1,1,1,1,1)),
            },
            "publication":{
                (1,1,1,None,None,None,None,None,None,None,None,None,None,None)
            },
            "publication_authors" :{
                (1,1,1,0),
                (2,1,2,1)

            }
        }
        result = create_publication(1,[1,2],database=TESTDB)
        self.assertEqual(result[0],1)
        compare_tables(self,test_success,ignore_id=True)

    def test_existing_publication(self):
        setup_database(TESTDB)
        insert_data("INSERT INTO cluster (id,cluster_name) VALUES(1,'random Title')")
        insert_data("INSERT into authors (id,main_name,block_name)"
                    "VALUES(1,'Nina Nonsense','nonsense,n'),(2,'Otto Otter','otter,o')")

        insert_data("INSERT INTO global_url(id,domain,url) VALUES(5,'x','x')")
        insert_data("INSERT INTO local_url(id,global_url_id,url) VALUES(5,5,'bla')")

        insert_data("INSERT INTO publication(id,url_id,cluster_id) VALUES (5,5,1)")
        result = create_publication(1, [1, 2], database=TESTDB)
        test_success = {
            "publication_authors": {
                (1, 5, 1, 0),
                (2, 5, 2, 1)

            }
        }
        self.assertEqual(result[0], 5)
        compare_tables(self, test_success, ignore_id=True)

    def tearDown(self):
        delete_database(TESTDB)
        pass

class TestCreateTitle(TestCase):
    def test_single_match(self):
        setup_database(TESTDB)
        insert_data("INSERT INTO cluster (id,cluster_name) VALUES(1,'matching title')")
        title = "matching title"
        matching = {
            "status": Status.SAFE,
            "match": Match.SINGLE_MATCH,
            "id": 1,
            "reason": None,
        }

        result = create_title(matching,title, database=TESTDB)
        self.assertEqual(result,1)

    def test_no_match(self):
        setup_database(TESTDB)
        title = "matching title"
        matching = {
            "status": Status.SAFE,
            "match": Match.NO_MATCH,
            "id": None,
            "reason": None,
        }

        test_success = {
            "cluster": {
                (1, "matching title"),
            },
        }
        result = create_title(matching,title, database=TESTDB)
        self.assertEqual(result, 1)
        compare_tables(self,test_success, ignore_id=True)

    def tearDown(self):
        delete_database(TESTDB)
        pass


class TestCreateAuthors(TestCase):
    def test_success(self):
        setup_database(TESTDB)
        #setup test data in db
        insert_data("INSERT into global_url (id,domain,url) VALUES(5,'a','a')")
        insert_data("INSERT into local_url (id,url,global_url_id) VALUES(1,'a',5)")
        insert_data("INSERT into authors (id,main_name,block_name)"
                    "VALUES(1,'Nina Nonsense','nonsense,n'),(2,'Otto Otter','otter,o'),(3,'Orna Otter','otter,o')")
        insert_data("INSERT into name_alias(id,authors_id,alias)"
                    "VALUES(1,1,'Nina Nonsense'),(2,2,'Otto Otter'),(3,3,'Orna Otter')")
        authors_list=[{
            "original_name": "Melvin Master",
            "parsed_name": "Melvin Master",
            "website": None,
            "contact": None,
            "about": None,
            "modified": None,
            "orcid_id": None,
            },
            {
                "original_name": "Nina Nonsense",
                "parsed_name": "Nina Nonsense",
                "website": None,
                "contact": None,
                "about": None,
                "modified": None,
                "orcid_id": None,
            },
            {
                "original_name": "Otto Otter",
                "parsed_name": "Otto Otter",
                "website": None,
                "contact": None,
                "about": None,
                "modified": None,
                "orcid_id": None,
            }
        ]
        matching_list=[
            {
                "status": Status.SAFE,
                "match": Match.NO_MATCH,
                "id": None,
                "reason": None,
            },
            {
                "status": Status.SAFE,
                "match": Match.SINGLE_MATCH,
                "id": 1,
                "reason": None,
            },
            {
                "status": Status.SAFE,
                "match": Match.MULTI_MATCH,
                "id": 2,
                "reason": None,
            }
        ]

        #resulting databasecontent
        test_success = {
            "authors": {
                (1, "Nina Nonsense", "nonsense,n", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
                (2, "Otto Otter", "otter,o", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
                (3, "Orna Otter", "otter,o", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
                (4, "Melvin Master", "master,m", None, None, None, datetime.datetime(1990, 1, 1, 1, 1, 1), None),
            },
            "name_alias": {
                (1, 1, "Nina Nonsense"),
                (2, 2, "Otto Otter"),
                (3, 3, "Orna Otter"),
                (4, 4, "Melvin Master"),
            },
            "alias_source": {
                (3, 1, 1),
                (5, 1, 2),
                (1, 1, 4),
            },
            "publication_authors": {
                (1, 1, 4, 0),
                (2, 1, 1, 1),
                (3, 1, 2, 2),
            }

        }
        result = create_authors(matching_list, authors_list,1, TESTDB)
        self.assertEqual(result,[4,1,2])
        compare_tables(self, test_success, ignore_id=True)

    def tearDown(self):
        delete_database(TESTDB)
