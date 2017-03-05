import datetime
from unittest import TestCase, mock

from dblp.xml_parser import  parse_xml
from tests.tools.Mariadb_stub import Mariadb_test
from harvester.exception import IHarvest_Exception
import logging


class TestParse_xml(TestCase):
    valid_dtd = "files/test.dtd"
    valid_xml = "files/valid.xml"
    valid_sql = None
    valid_tag_list = ("article", "inproceedings")
    valid_start_date_1 = "1992-1-31"
    valid_start_date_2 = datetime.datetime(1991, 1, 31)
    valid_end_date_1 = "1992-2-15"
    valid_end_date_2 = datetime.datetime(2012, 2, 15)
    valid_logger = logging.getLogger("test")

    def test_taglist_fail(self):
        self.assertRaises(IHarvest_Exception, parse_xml, self.valid_xml, self.valid_dtd,
                          self.valid_sql, self.valid_logger, 123)

    def test_startdate_fail(self):
        self.assertRaises(IHarvest_Exception, parse_xml, self.valid_xml, self.valid_dtd, self.valid_sql,
                          self.valid_logger, self.valid_tag_list, 123)

    def test_enddate_fail_1(self):
        self.assertRaises(IHarvest_Exception, parse_xml, self.valid_xml, self.valid_dtd, self.valid_sql,
                          self.valid_logger, self.valid_tag_list, self.valid_start_date_1, 123)

    def test_enddate_fail_2(self):
        self.assertRaises(IHarvest_Exception, parse_xml, self.valid_xml, self.valid_dtd, self.valid_sql,
                          self.valid_logger, self.valid_tag_list, self.valid_start_date_2,"haha")

    def test_xml_fail(self):
        self.assertRaises(IHarvest_Exception, parse_xml, "files/bla.bla", self.valid_dtd, self.valid_sql,
                          self.valid_logger, self.valid_tag_list, self.valid_start_date_2, self.valid_end_date_1)

    def test_dtd_fail(self):
        self.assertRaises(IHarvest_Exception, parse_xml, self.valid_xml, "files/bla.bla", self.valid_sql,
                          self.valid_logger, self.valid_tag_list, self.valid_start_date_2, self.valid_end_date_2)

    def test_sql_fail(self):
        self.assertRaises(IHarvest_Exception, parse_xml, self.valid_xml, self.valid_dtd, None,
                          self.valid_logger, self.valid_tag_list, self.valid_start_date_2, self.valid_end_date_2)

    def test_invalid_mdate(self):
        test_db = Mariadb_test()
        self.assertEqual(1,parse_xml("files/invalid-mdate.xml", self.valid_dtd, test_db,
                          self.valid_logger, self.valid_tag_list, self.valid_start_date_2, self.valid_end_date_2))

    def test_invalid_year(self):
        test_db = Mariadb_test()
        self.assertEqual(1,parse_xml("files/invalid-year.xml", self.valid_dtd, test_db,
                          self.valid_logger, self.valid_tag_list, self.valid_start_date_2, self.valid_end_date_2))

    @mock.patch.object(Mariadb_test, 'execute')
    def test_article_valid(self,mock_execute):
        test_db = Mariadb_test()
        result =parse_xml(self.valid_xml, self.valid_dtd, test_db,self.valid_logger,
                                          self.valid_tag_list,self.valid_start_date_2, self.valid_end_date_2)
        mock_execute.assert_called_with(
                                        ('journals/acta/Saxena96', datetime.datetime(2011, 1, 11, 0, 0), 'Sanjeev Saxena;',
                                         'Parallel Integer Sorting and Simulation Amongst CRCW Models.', '607-619',
                                         datetime.datetime(1996, 1, 1, 0, 0), '33', 'Acta Inf.', '7',
                                         'http://dx.doi.org/10.1007/BF03036466', 'db/journals/acta/acta33.html#Saxena96',
                                         None, None, None,None,None,None,None,None,'article')
                                        )
        self.assertEqual(result, 1)

    def test_time_range_0(self):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-timerange-n.xml", self.valid_dtd, test_db, self.valid_logger,
                                          self.valid_tag_list,"2013-02-01", "2013-02-28")
        self.assertEqual(result,0)

    def test_time_range_n(self):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-timerange-n.xml", self.valid_dtd, test_db, self.valid_logger,
                                          self.valid_tag_list,"2012-02-01", "2012-02-28")
        self.assertEqual(result,2)
        self.assertListEqual(["a/b/c", "d/e/f"], test_db.getList())
        pass

    @mock.patch.object(Mariadb_test, 'execute')
    def test_tag_in_title(self, mock_execute):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-title.xml", self.valid_dtd, test_db, self.valid_logger)
        self.assertEqual(result, 1)
        mock_execute.assert_called_with(
                                        ('a/b/c', datetime.datetime(2012, 2, 12, 0, 0), 'Aut hor;', 'title of titles',
                                         '607-619',
                                         datetime.datetime(1996, 1, 1, 0, 0), '33', 'Acta Inf.', '7',
                                         'http://dx.doi.org/10.1007/BF03036466',
                                         'db/journals/acta/acta33.html#Saxena96', None, None, None,
                                         None, None, None, None, None, 'article')
                                        )
    @mock.patch.object(Mariadb_test, 'execute')
    def test_tag_in_title_regression(self, mock_execute):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-title2.xml", self.valid_dtd, test_db, self.valid_logger)
        self.assertEqual(result, 1)
        mock_execute.assert_called_with(
                                        ('journals/kbs/FinnieS03', datetime.datetime(2004, 5, 4, 0, 0),
                                         'Gavin R. Finnie;Zhaohao Sun;', 'R5 model for case-based reasoning.', '59-65',
                                         datetime.datetime(2003, 1, 1, 0, 0), '16', 'Knowl.-Based Syst.', '1',
                                         'http://dx.doi.org/10.1016/S0950-7051(02)00053-9',
                                         'db/journals/kbs/kbs16.html#FinnieS03', None, None,
                                         None,None,None,None,None,None,'article')
                                        )
    @mock.patch.object(Mariadb_test, 'execute')
    def test_tag_in_title_regression2(self, mock_execute):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-title3.xml", self.valid_dtd, test_db, self.valid_logger)
        self.assertEqual(result, 1)

        mock_execute.assert_called_with(
                                        ('journals/acs/GrandjeanL03', datetime.datetime(2006, 5, 29, 0, 0), 'A. R. Grandjeán;M. P. López;',
                                         'H2q(T, G, delta) and q-perfect Crossed Modules.', '171-184', datetime.datetime(2003, 1, 1, 0, 0), '11',
                                         'Applied Categorical Structures', '2', 'http://dx.doi.org/10.1023/A:1023507229607',
                                         'db/journals/acs/acs11.html#GrandjeanL03', None, None, None,
                                         None,None,None,None,None,'article')
                                        )

    @mock.patch.object(Mariadb_test, 'execute')
    def test_tag_in_title_regression4(self, mock_execute):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-title4.xml", self.valid_dtd, test_db, self.valid_logger)
        self.assertEqual(result, 1)

        mock_execute.assert_called_with(
                ('journals/tkde/PangZM13', datetime.datetime(2015, 9, 9, 0, 0),
                 'HweeHwa Pang;Jilian Zhang;Kyriakos Mouratidis;',
                 'Enhancing Access Privacy of Range Retrievals over B+)-Trees.', '1533-1547',
                 datetime.datetime(2013, 1, 1, 0, 0), '25', 'IEEE Trans. Knowl. Data Eng.',
                 '7', 'http://doi.ieeecomputersociety.org/10.1109/TKDE.2012.77',
                 'db/journals/tkde/tkde25.html#PangZM13', None, None, None,None,None,None,None,None,'article')
        )






    @mock.patch.object(Mariadb_test, 'execute')
    def test_multiple_authors(self, mock_execute):
        test_db = Mariadb_test()
        result =parse_xml("files/valid-authors.xml", self.valid_dtd, test_db, self.valid_logger,("article","inproceedings"))
        self.assertEqual(result, 1)
        mock_execute.assert_called_with(
                                        ('a/b/c', datetime.datetime(2012, 2, 12, 0, 0), 'Aut hor;AutA horA;AutB horB;AutC horC;',
                                         'title of titles','607-619',
                                         datetime.datetime(1996, 1, 1, 0, 0), '33', 'Acta Inf.', '7',
                                         'http://dx.doi.org/10.1007/BF03036466',
                                         'db/journals/acta/acta33.html#Saxena96', None, None, None,
                                         None, None, None, None, None, 'article')
                                        )

    def test_article_valid_min(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-min.xml", self.valid_dtd, test_db, self.valid_logger)
        self.assertEqual(result, 1)

    def test_article_valid_max(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-full.xml", self.valid_dtd, test_db, self.valid_logger)
        self.assertEqual(result,1)

    def test_inproceedings_article(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-tags.xml", self.valid_dtd, test_db, self.valid_logger)
        self.assertEqual(result, 2)

    def test_limit_0(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-limit.xml", self.valid_dtd, test_db, self.valid_logger, limit=0)
        self.assertEqual(result, 0)

    def test_limit_1(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-limit.xml", self.valid_dtd, test_db, self.valid_logger, limit=1)
        self.assertEqual(result, 1)

    def test_limit_max(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-limit.xml", self.valid_dtd, test_db, self.valid_logger, limit=99)
        self.assertEqual(result, 5)

    def test_limit_equal(self):
        test_db = Mariadb_test()
        result = parse_xml("files/valid-limit.xml", self.valid_dtd, test_db, self.valid_logger, limit=5)
        self.assertEqual(result, 5)



