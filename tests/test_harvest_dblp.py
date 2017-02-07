from unittest import TestCase
from harvester.IHarvester import IHarvest
from harvester.exception import IHarvest_Exception

from dblp.dblpharvester import DblpHarvester


class Test_Dblp_Harvester(TestCase):

    def test_invalid_xml_ini(self):
        self.assertRaises(IHarvest_Exception,DblpHarvester,path="files/DH1.ini")

    def test_invalid_dtd_ini(self):
        self.assertRaises(IHarvest_Exception,DblpHarvester,path="files/DH2.ini")

    def test_invalid_tags_ini(self):
        self.assertRaises(IHarvest_Exception,DblpHarvester,path="files/DH3.ini")

    def test_invalid_database_ini(self):
        self.assertRaises(IHarvest_Exception,DblpHarvester,path="files/DH4.ini")

    def test_valid_ini(self):
        x = DblpHarvester(path="files/DH5.ini")
        self.assertEqual(x.tags, ('article', 'inproceedings'))
