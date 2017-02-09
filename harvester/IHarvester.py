from abc import ABC, abstractmethod
from .exception import IHarvest_Exception, IHarvest_Disabled
import configparser
import os.path
import logging
from celery.utils.log import get_task_logger
from mysqlWrapper.mariadb import MariaDb

#TODO logs entfernen, da sie durch exceptions redundant sind
class IHarvest(ABC):
    HARVESTER_PATH = "harvester.ini"

    def __init__(self, name, celery=False):
        self.name = name
        # set logger
        if celery:
            self.logger = get_task_logger(name)
        else:
            self.logger = logging.getLogger(name)

        # load config
        self.config = configparser.ConfigParser()
        self.config.read(self.HARVESTER_PATH)
        if name not in self.config:
            self.logger.critical("Error: Config could not be loaded")
            raise IHarvest_Exception("Error: Config could not be loaded for name " + name)
        if "MARIADB" not in self.config:
            self.logger.critical("MARIADB ERROR: Missing Credentials in Config")
            raise IHarvest_Exception("")

        # connect to database
        credentials = dict(self.config["MARIADB"])
        try:
            self.connector = MariaDb(credentials)
            self.logger.debug("MariaDB connection successful")
        except Exception as err:
            self.logger.critical("MARIADB ERROR: %s", err)
            raise IHarvest_Exception("")
        # check certain parameters in specific config
        self.configValues = dict(self.config[name])

        #check enabled
        try:
            self.enabled = self.config[name].getboolean("enabled")
            if self.enabled is None:
                raise KeyError()
        except KeyError as e:
            self.logger.critical("Config value %s missing", e)
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
                self.logger.critical("Invalid limit")
                raise IHarvest_Exception("Error: Invalid limit")
        else:
            self.limit = None

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self, time_begin=None, time_end=None):
        pass
