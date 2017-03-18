from unittest import TestCase
from tasks.ingest_task import ingest_task
from pub_storage.exception import IIngester_Exception, IIngester_Disabled


class TestIngestTask(TestCase):

    def test_invalid_module(self):
        self.assertRaises(AttributeError,ingest_task,"dblp.dblpingester","DblpInester", config_path="ingest_task.ini")
        # self.assertTrue(ingest_task("dblp.dblpingester", "DblpIngester", config_path="blub"))

    def test_invalid_module_path(self):
        self.assertRaises(ImportError,ingest_task,"dblp.dblpingestr","DblpIngester", config_path="ingest_task.ini")

    def test_invalid_module_class(self):
        self.assertRaises(IIngester_Exception, ingest_task,"harvester.exception", "IHarvest_Disabled",
                          config_path="ingest_task.ini")

    def test_invalid_enabled(self):
        self.assertRaises(IIngester_Exception, ingest_task,"dblp.dblpingester","DblpIngester",
                          config_path="ingest_task2.ini")

    def test_disabled(self):
        self.assertRaises(IIngester_Disabled, ingest_task,"dblp.dblpingester","DblpIngester",
                          config_path="ingest_task3.ini")

    def test_valid_limit(self):
        # TODO
        # self.assertTrue(ingest_task("dblp.dblpingester", "DblpIngester", config_path="ingest_task.ini"))
        pass





