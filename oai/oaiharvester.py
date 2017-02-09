from harvester.IHarvester import IHarvest
from harvester.exception import IHarvest_Exception

from oai.queries import OAI_DATASET
from harvester.exception import IHarvest_Exception
from oai.oaimph_parser import harvestOAI


NAME = "OAI_HARVESTER"


class OaiHarvester(IHarvest):

    def __init__(self, celery=False, path=None):
        # mainly for testing
        if path is not None:
            self.HARVESTER_PATH = path
        # call constructor of base class for initiating values
        IHarvest.__init__(self, NAME, celery)

        # get config values
        # required values
        try:
            self.link = self.configValues["link"]
            self.table_name = self.configValues["table_name"]
            self.enabled = self.configValues["enabled"]
        except KeyError as e:
            self.logger.critical("Config value %s missing", e)
            raise IHarvest_Exception("Error: config value {} not found".format(e))

        # optional values
        if "limit" in self.configValues:
            self.limit = int(self.configValues["limit"])
            #TODO try catch
        else:
            self.limit = None

    def init(self):
        # create database if not available
        if self.connector.createTable(self.table_name, OAI_DATASET):
            self.logger.info("Table %s created", self.table_name)
            return True
        else:
            self.logger.critical("Table could not be created")
            return False

    #TODO
    # time_begin and time_end are always valid datetime objects
    def run(self, time_begin=None, time_end=None):
        if self.enabled is False:
            self.logger.info("Task %s is disabled", self.name)
            return 0
        #return parse_xml(self.xml_path, self.dtd_path, self.connector, self.logger, self.tags, time_begin, time_end, self.limit)



