from unittest import TestCase, mock

from dblp.xml_parser import  parse_xml
from dblp.queries import  ADD_DBLP_ARTICLE
from mysqlWrapper.mariadb import MariaDb
import datetime


class Mariadb_test(MariaDb):

    def __init__(self):
        pass

    def execute(self,a,b):
        return True
    def close_connection(self):
        pass


class TestParse_xml(TestCase):
    valid_dtd = "files/test.dtd"
    valid_xml = "files/valid.xml"
    valid_sql = None
    valid_tag_list = "article"
    valid_start_date_1 = "1992-1-31"
    valid_start_date_2 = datetime.datetime(1991,1,31)
    valid_end_date_1 = "1992-2-15"
    valid_end_date_2 = datetime.datetime(2012,2,15)

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

    @mock.patch.object(Mariadb_test,'execute')
    def test_article_valid(self,mock_execute):
        test_db = Mariadb_test()
        result =parse_xml(self.valid_xml, self.valid_dtd, test_db,
                                          self.valid_tag_list,self.valid_start_date_2, self.valid_end_date_2)
        mock_execute.assert_called_with(ADD_DBLP_ARTICLE,
                                        ('journals/acta/Saxena96', datetime.datetime(2011, 1, 11, 0, 0), 'Sanjeev Saxena;',
                                         'Parallel Integer Sorting and Simulation Amongst CRCW Models.', '607-619',
                                         datetime.datetime(1996, 1, 1, 0, 0), '33', 'Acta Inf.', '7',
                                         'http://dx.doi.org/10.1007/BF03036466', 'db/journals/acta/acta33.html#Saxena96', None, None, None)
                                        )
        self.assertEqual(result, True)
        pass

    def test_time_range_0(self):
        pass

    def test_time_range_n(self):
        pass

    def test_tag_in_title(self):
        pass

    def test_multiple_authors(self):
        pass

    def test_article_valid_min(self):
        pass

    def test_article_valid_max(self):
        pass

    #TODO add other types
