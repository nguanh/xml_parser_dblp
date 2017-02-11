from harvester.IHarvester import IHarvest
from oai.queries import OAI_DATASET
from harvester.exception import IHarvest_Exception
from oai.oaimph_parser import harvestOAI


class OaiHarvester(IHarvest):

    def __init__(self, name, celery=False, path=None):
        # mainly for testing
        if path is not None:
            self.HARVESTER_PATH = path
        # call constructor of base class for initiating values
        IHarvest.__init__(self, name, celery)

        # get config values
        # required values
        try:
            self.link = self.configValues["link"]
            self.table_name = self.configValues["table_name"]
        except KeyError as e:
            self.logger.critical("Config value %s missing", e)
            raise IHarvest_Exception("Error: config value {} not found".format(e))

    def init(self):
        # create database if not available
        if self.connector.createTable(self.table_name, OAI_DATASET):
            self.logger.info("Table %s created", self.table_name)
            return True
        else:
            self.logger.critical("Table could not be created")
            return False

    # time_begin and time_end are always valid datetime objects
    def run(self, time_begin=None, time_end=None):
        return harvestOAI(self.link, self.connector, self.logger,
                          startDate=time_begin, endDate=time_end, limit=self.limit)



