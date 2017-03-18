from unittest import TestCase

from pub_storage.setup_database import setup_database
from pub_storage.Iingester import Iingester
from pub_storage.exception import IIngester_Exception
from pub_storage.ingester import create_authors, create_title, create_publication, update_diff_tree
from .ingester_tools import TESTDB, delete_database, insert_data, compare_tables, get_pub_dict
from pub_storage.helper import *
from mysqlWrapper.mariadb import MariaDb
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



