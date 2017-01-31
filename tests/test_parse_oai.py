from unittest import TestCase, mock

from oai.oaimph_parser import  harvestOAI
from oai.queries import ADD_OAI_DEFAULT
from .tools.Mariadb_stub import Mariadb_test
import datetime


class TestParseOai(TestCase):
    valid_link = 'http://citeseerx.ist.psu.edu/oai2'

    def test_sql_fail(self):
        result = harvestOAI(self.valid_link,None)
        self.assertEqual(result,(False,0))
        pass

    def test_link_fail(self):
        test_db = Mariadb_test()
        result = harvestOAI("hkjlkj",test_db)
        self.assertEqual(result, (False, 0))

    def test_parameter_fail(self):
        test_db = Mariadb_test()
        result = harvestOAI(self.valid_link,test_db,startDate="98790",endDate="gjhhk")
        self.assertEqual(result, (False, 0))

    def test_no_results(self):
        test_db = Mariadb_test()
        result = harvestOAI(self.valid_link,test_db,startDate="1900-01-01",endDate="1900-01-01")
        self.assertEqual(result, (False, 0))

    def test_valid(self):
        test_db = Mariadb_test()
        result = harvestOAI(self.valid_link, test_db, startDate="2013-01-01", endDate="2013-01-01")
        self.assertEqual(result, (True, 1))
        self.assertEqual((test_db.getList()[0]), 'http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.251.2812;')

