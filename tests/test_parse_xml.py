from unittest import TestCase, mock

from dblp.xml_parser import  parse_xml
from dblp.queries import  ADD_DBLP_ARTICLE
from mysqlWrapper.mariadb import MariaDb
import datetime


class Mariadb_test(MariaDb):

    def __init__(self):
        self.list = []
        pass

    def execute(self,a,b):
        # append key to list
        self.list.append(b[0])
        return True

    def getList(self):
        return self.list

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
        self.assertEqual((False, 0), parse_xml(self.valid_xml,self.valid_dtd,self.valid_sql, 123))

    def test_startdate_fail(self):
        self.assertEqual((False, 0), parse_xml(self.valid_xml, self.valid_dtd, self.valid_sql, self.valid_tag_list,123))

    def test_enddate_fail_1(self):
        self.assertEqual((False, 0), parse_xml(self.valid_xml, self.valid_dtd, self.valid_sql, self.valid_tag_list,self.valid_start_date_1,123))

    def test_enddate_fail_2(self):
        self.assertEqual((False, 0), parse_xml(self.valid_xml, self.valid_dtd, self.valid_sql, self.valid_tag_list,self.valid_start_date_2,"haha"))

    def test_xml_fail(self):
        self.assertEqual((False, 0), parse_xml("files/bla.bla", self.valid_dtd, self.valid_sql,
                                          self.valid_tag_list,self.valid_start_date_2,self.valid_end_date_1))

    def test_dtd_fail(self):
        self.assertEqual((False, 0), parse_xml(self.valid_xml, "files/bla.bla", self.valid_sql,
                                          self.valid_tag_list,self.valid_start_date_2,self.valid_end_date_2))

    def test_sql_fail(self):
        self.assertEqual((False, 0), parse_xml(self.valid_xml, self.valid_dtd, None,
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
        self.assertEqual(result, (True, 1))
        pass

    def test_time_range_0(self):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-timerange-n.xml", self.valid_dtd, test_db,
                                          self.valid_tag_list,"2013-02-01", "2013-02-28")
        self.assertEqual(result,(True,0))

    def test_time_range_n(self):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-timerange-n.xml", self.valid_dtd, test_db,
                                          self.valid_tag_list,"2012-02-01", "2012-02-28")
        self.assertEqual(result,(True,2))
        self.assertListEqual(["a/b/c", "d/e/f"], test_db.getList())
        pass

    @mock.patch.object(Mariadb_test, 'execute')
    def test_tag_in_title(self, mock_execute):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-title.xml", self.valid_dtd, test_db)
        self.assertEqual(result, (True, 1))
        mock_execute.assert_called_with(ADD_DBLP_ARTICLE,
                                        ('a/b/c', datetime.datetime(2012, 2, 12, 0, 0), 'Aut hor;', 'title of titles',
                                         '607-619',
                                         datetime.datetime(1996, 1, 1, 0, 0), '33', 'Acta Inf.', '7',
                                         'http://dx.doi.org/10.1007/BF03036466',
                                         'db/journals/acta/acta33.html#Saxena96', None, None, None)
                                        )

    @mock.patch.object(Mariadb_test, 'execute')
    def test_multiple_authors(self, mock_execute):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-authors.xml", self.valid_dtd, test_db)
        self.assertEqual(result, (True, 1))
        mock_execute.assert_called_with(ADD_DBLP_ARTICLE,
                                        ('a/b/c', datetime.datetime(2012, 2, 12, 0, 0), 'Aut hor;AutA horA;AutB horB;AutC horC;',
                                         'title of titles','607-619',
                                         datetime.datetime(1996, 1, 1, 0, 0), '33', 'Acta Inf.', '7',
                                         'http://dx.doi.org/10.1007/BF03036466',
                                         'db/journals/acta/acta33.html#Saxena96', None, None, None)
                                        )

    def test_article_valid_min(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-min.xml", self.valid_dtd, test_db)
        self.assertEqual(result, (True, 1))

    def test_article_valid_max(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-full.xml", self.valid_dtd, test_db)
        self.assertEqual(result, (True, 1))

    def test_inproceedings_article(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-tags.xml", self.valid_dtd, test_db)
        self.assertEqual(result, (True, 2))
