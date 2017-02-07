from unittest import TestCase
from harvester.IHarvester import IHarvest
from harvester.exception import IHarvest_Exception

class H1 (IHarvest):
    def __init__(self):
        self.HARVESTER_PATH= "xxx"
        IHarvest.__init__(self, "h1", False)
    def init(self):
        pass
    def run(self):
        pass

class H2 (IHarvest):
    def __init__(self):
        self.HARVESTER_PATH= "files/h1.ini"
        IHarvest.__init__(self, "h2", False)
    def init(self):
        pass
    def run(self):
        pass

class H3 (IHarvest):
    def __init__(self):
        self.HARVESTER_PATH= "files/h1.ini"
        IHarvest.__init__(self, "h1", False)
    def init(self):
        pass
    def run(self):
        pass

class H4 (IHarvest):
    def __init__(self):
        self.HARVESTER_PATH= "files/h2.ini"
        IHarvest.__init__(self, "h1", False)
    def init(self):
        pass
    def run(self):
        pass

class H5 (IHarvest):
    def __init__(self):
        self.HARVESTER_PATH= "files/h3.ini"
        IHarvest.__init__(self, "h1", False)
    def init(self):
        pass
    def run(self):
        pass


class TestIHarvest(TestCase):
    def test_h1(self):
        # invalid path
        self.assertRaises(IHarvest_Exception,H1)
    def test_h2(self):
        # invalid name
        self.assertRaises(IHarvest_Exception,H2)
    def test_h3(self):
        #no credentials
        self.assertRaises(IHarvest_Exception,H3)
    def test_h4(self):
        #missing username in credentials
        self.assertRaises(IHarvest_Exception,H4)
    def test_h5(self):
        #all valid
        H5()

