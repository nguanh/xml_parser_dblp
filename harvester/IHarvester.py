from abc import ABC, abstractmethod
from .exception import IHarvest_Exception
import configparser
import os.path
import logging
from celery.utils.log import get_task_logger
from mysqlWrapper.mariadb import MariaDb


class IHarvest(ABC):
    HARVESTER_PATH = "../harvester.ini"

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
        self.configValues = dict(self.config[name])
        credentials = dict(self.config["MARIADB"])
        try:
            self.connector = MariaDb(credentials)
            self.logger.debug("MariaDB connection successful")
        except Exception as err:
            self.logger.critical("MARIADB ERROR: %s", err)
            raise IHarvest_Exception("")


    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self, time_begin=None, time_end=None):
        pass
