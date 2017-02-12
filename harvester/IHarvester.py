from abc import ABC, abstractmethod
from .exception import IHarvest_Exception, IHarvest_Disabled
import configparser
from mysqlWrapper.mariadb import MariaDb

class IHarvest(ABC):
    HARVESTER_PATH = "harvester.ini"

    def __init__(self, logger, name):
        self.name = name
        self.logger = logger

        logger.info("Success")
        # load config
        self.config = configparser.ConfigParser()
        self.config.read(self.HARVESTER_PATH)
        if name not in self.config:
            raise IHarvest_Exception("Error: Config could not be loaded for " + name)
        if "MARIADB" not in self.config:
            raise IHarvest_Exception("MARIADB ERROR: Missing Credentials in Config")

        # connect to database
        credentials = dict(self.config["MARIADB"])
        try:
            self.connector = MariaDb(credentials)
            self.logger.debug("MariaDB connection successful")
        except Exception as err:
            raise IHarvest_Exception("MARIADB ERROR: {}".format(err))
        # check certain parameters in specific config
        self.configValues = dict(self.config[name])

        #check enabled
        try:
            self.enabled = self.config[name].getboolean("enabled")
            if self.enabled is None:
                raise KeyError()
        except KeyError as e:
            raise IHarvest_Exception("Error: config value {} not found".format(e))

        if self.enabled is False:
            self.connector.close_connection()
            raise IHarvest_Disabled()
        # check optional limit
        if "limit" in self.configValues:
            try:
                self.limit = int(self.configValues["limit"])
                if self.limit < 0:
                    raise
            except:
                raise IHarvest_Exception("Error: Invalid limit")
        else:
            self.limit = None

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self, time_begin=None, time_end=None):
        pass
