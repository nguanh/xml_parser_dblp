from abc import ABC, abstractmethod
from .exception import IHarvest_Exception
import configparser
import os.path
import logging
from celery.utils.log import get_task_logger
from mysqlWrapper.mariadb import MariaDb


class IHarvest(ABC):
    HARVESTER_PATH = "harvester.ini"

    def __init__(self, name, celery=False):
        self.name = name
        # set logger
        if celery:
            self.logger = get_task_logger(name)
        else:
            self.logger = logging.getLogger(name)

        # get config path
        parent_path = os.path.dirname(os.path.dirname(__file__))
        ini_path = os.path.join(parent_path, self.HARVESTER_PATH)

        # load config
        self.config = configparser.ConfigParser()
        self.config.read(ini_path)
        try:
            self.configValues = dict(self.config[name])
            self.logger.debug("Config found")
        except KeyError:
            self.logger.exception("Error: Config could not be loaded")
            raise IHarvest_Exception("Error: Config could not be loaded for name" + name)

        # connect to database
        credentials = dict(self.config["MARIADB"])
        try:
            self.database = MariaDb(credentials)
            self.logger.debug("MariaDB connection successful")
        except Exception as err:
            self.logger.exception("MARIADB ERROR: %s", err)
            raise IHarvest_Exception()

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def run(self, time_begin=None, time_end=None):
        pass
