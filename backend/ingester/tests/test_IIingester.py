from unittest import TestCase

from backend.ingester.setup_database import setup_database
from backend.ingester.Iingester import Iingester
from backend.ingester.exception import IIngester_Exception
from backend.ingester.ingester import create_authors, create_title, create_publication, update_diff_tree
from .ingester_tools import TESTDB, delete_database, insert_data, compare_tables, get_pub_dict
from backend.ingester.helper import *
from backend.mysqlWrapper.mariadb import MariaDb
import datetime


class Dummy (Iingester):
    def __init__(self):
        Iingester.__init__(self)
        self.query = "SELECT * FROM test"

    def get_global_url(self):
        pass

    def mapping_function(self, query_dataset):
        pass
    def update_harvested(self):
        pass

    def get_name(self):
        pass


class TestIIngester(TestCase):

    def test_set_limit_invalid1(self):
        tmp = Dummy()
        self.assertRaises(IIngester_Exception,tmp.set_limit,"Hallo")

    def test_set_limit_invalid1(self):
        tmp = Dummy()
        self.assertRaises(IIngester_Exception,tmp.set_limit,0)

    def test_get_query_no_limit(self):
        tmp = Dummy()
        result = tmp.get_query()
        self.assertEqual(result, "SELECT * FROM test")

    def test_get_query_limit(self):
        tmp = Dummy()
        tmp.set_limit(100)
        result = tmp.get_query()
        self.assertEqual(result, "SELECT * FROM test LIMIT 100")



