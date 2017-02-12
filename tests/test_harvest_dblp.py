from unittest import TestCase
from harvester.exception import IHarvest_Exception

from dblp.dblpharvester import DblpHarvester
import  logging


class Test_Dblp_Harvester(TestCase):
    name = "DBLP_HARVESTER"
    logger = logging.getLogger("TEST")
    def test_invalid_xml_ini(self):
        self.assertRaises(IHarvest_Exception, DblpHarvester, self.logger, self.name, path="files/DH1.ini")

    def test_invalid_dtd_ini(self):
        self.assertRaises(IHarvest_Exception, DblpHarvester, self.logger, self.name, path="files/DH2.ini")

    def test_invalid_tags_ini(self):
        self.assertRaises(IHarvest_Exception, DblpHarvester, self.logger, self.name, path="files/DH3.ini")

    def test_invalid_database_ini(self):
        self.assertRaises(IHarvest_Exception, DblpHarvester, self.logger, self.name, path="files/DH4.ini")

    def test_valid_ini(self):
        x = DblpHarvester(self.logger, self.name, path="files/DH5.ini")
        self.assertEqual(x.tags, ('article', 'inproceedings'))

    def test_valid_init(self):
        x = DblpHarvester(self.logger, self.name, path="files/DH5.ini")
        self.assertEqual(x.init(),True)

    def test_invalid_init(self):
        x = DblpHarvester(self.logger, self.name, path="files/DH6.ini")
        self.assertEqual(x.init(),False)

    def test_invalid_run(self):
        x = DblpHarvester(self.logger, self.name, path="files/DH6.ini")
        x.init()
        self.assertRaises(IHarvest_Exception, x.run)

