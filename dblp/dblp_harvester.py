from harvester.IHarvester import IHarvest
from harvester.exception import IHarvest_Exception

from dblp.queries import DBLP_ARTICLE
from dblp.exception import Dblp_Parsing_Exception


class dblp_harvester(IHarvest):

    def __init__(self, name, celery=False):
        # call constructor of base class for initiating values
        IHarvest.__init__(self, name,celery)

        # get config values
        try:
            self.xml_path = self.configValues["xml_path"]
            self.dtd_path = self.configValues["dtd_path"]
            self.tags = self.configValues["tags"]
            self.table_name = self.configValues["table_name"]
        except KeyError as e:
            self.logger.exception("Config value %s missing", e)
            raise IHarvest_Exception("Error: config value {} not found".format(e))

        # convert tags to tuple
        self.tags = tuple(self.tags.split(","))

    def init(self):
        # create database if not available
        if self.database.createTable(self.table_name, DBLP_ARTICLE):
            self.logger.info("Table %s created", self.table_name)
            return True
        else:
            self.logger.critical("Table could not be created")
            return False


    def run(self,time_begin = None, time_end=None):
        pass







x= dblp_harvester("DBLP_HARVESTER")
print(x.init())