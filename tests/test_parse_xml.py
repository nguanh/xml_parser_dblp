from unittest import TestCase
from dblp.xml_parser import  parse_xml
import datetime


class TestParse_xml(TestCase):
    valid_dtd = "files/test.dtd"
    valid_xml = "files/test.dtd"
    valid_sql = None
    valid_tag_list = "article"
    valid_start_date_1 = "31-1-1992"
    valid_start_date_2 = datetime.datetime(1991,1,31)
    valid_end_date_1 = "15-2-1992"
    valid_end_date_2 = datetime.datetime(1991,2,15)

    def test_taglist_fail(self):
        self.assertEqual(False,parse_xml(self.valid_xml,self.valid_dtd,self.valid_sql, 123))

    def test_startdate_fail(self):
        self.assertEqual(False, parse_xml(self.valid_xml, self.valid_dtd, self.valid_sql, self.valid_tag_list,123))

    def test_enddate_fail_1(self):
        self.assertEqual(False, parse_xml(self.valid_xml, self.valid_dtd, self.valid_sql, self.valid_tag_list,self.valid_start_date_1,123))

    def test_enddate_fail_2(self):
        self.assertEqual(False, parse_xml(self.valid_xml, self.valid_dtd, self.valid_sql, self.valid_tag_list,self.valid_start_date_2,"haha"))

    def test_xml_fail(self):
        self.assertEqual(False, parse_xml("files/bla.bla", self.valid_dtd, self.valid_sql,
                                          self.valid_tag_list,self.valid_start_date_2,self.valid_end_date_1))

    def test_dtd_fail(self):
        self.assertEqual(False, parse_xml(self.valid_xml, "files/bla.bla", self.valid_sql,
                                          self.valid_tag_list,self.valid_start_date_2,self.valid_end_date_2))

    def test_sql_fail(self):
        self.assertEqual(False, parse_xml(self.valid_xml, self.valid_dtd, None,
                                          self.valid_tag_list,self.valid_start_date_2, self.valid_end_date_2))
