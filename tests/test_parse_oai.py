from unittest import TestCase, mock

from oai.oaimph_parser import  harvestOAI
from oai.queries import ADD_OAI_DEFAULT
from .tools.Mariadb_stub import Mariadb_test
from oai.exception import Oai_Parsing_Exception
import datetime


class TestParseOai(TestCase):
    valid_link = 'http://citeseerx.ist.psu.edu/oai2'

    def test_sql_fail(self):
        self.assertRaises(Oai_Parsing_Exception, harvestOAI, self.valid_link,None)

    def test_link_fail(self):
        test_db = Mariadb_test()
        self.assertRaises(Oai_Parsing_Exception, harvestOAI,"hkjlkj",test_db)

    def test_parameter_fail(self):
        test_db = Mariadb_test()
        self.assertRaises(Oai_Parsing_Exception, harvestOAI,self.valid_link,test_db,startDate="98790",endDate="gjhhk")

    def test_no_results(self):
        test_db = Mariadb_test()
        self.assertRaises(Oai_Parsing_Exception, harvestOAI,self.valid_link,test_db,startDate="1900-01-01",endDate="1900-01-01")


    def test_valid(self):
        test_db = Mariadb_test()
        result = harvestOAI(self.valid_link, test_db, startDate="2013-01-01", endDate="2013-01-01")
        self.assertEqual(result, 1)
        self.assertEqual((test_db.getList()[0]), 'http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.251.2812;')

