from unittest import TestCase
from tasks.harvest_task import harvest_task
from harvester.exception import IHarvest_Disabled,IHarvest_Exception


class TestHarvest_task(TestCase):

    def test_success(self):
        self.assertTrue(harvest_task("dblp.dblpharvester", "DblpHarvester", "DBLP_HARVESTER",
                                     path="harvest_task.ini"))

    def test_import_fail(self):
        self.assertRaises(ImportError,harvest_task,"dblp.dblpharXXXX", "DblpHarvester", "DBLP_HARVESTER",
                                     path="harvest_task.ini")

    def test_task_disabled(self):
        self.assertRaises(IHarvest_Disabled, harvest_task, "dblp.dblpharvester", "DblpHarvester", "DBLP_HARVESTER",
                          path="harvest_task2.ini")

    def test_instance_fail(self):
        # invalid xml path
        self.assertRaises(IHarvest_Exception, harvest_task, "dblp.dblpharvester", "DblpHarvester", "DBLP_HARVESTER",
                          path="harvest_task3.ini")

    def test_invalid_instance_fail(self):
        self.assertRaises(IHarvest_Exception, harvest_task, "harvester.exception", "IHarvest_Disabled", "DBLP_HARVESTER",
                          path="harvest_task3.ini")

    def test_init_fail(self):
        # no database is selected, tables can't be created on init --> fail
        self.assertRaises(IHarvest_Exception, harvest_task, "dblp.dblpharvester", "DblpHarvester", "DBLP_HARVESTER",
                          path="harvest_task4.ini")


