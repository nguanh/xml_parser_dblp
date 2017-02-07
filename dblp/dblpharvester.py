from harvester.IHarvester import IHarvest
from harvester.exception import IHarvest_Exception

from dblp.queries import DBLP_ARTICLE
from harvester.exception import IHarvest_Exception
from dblp.xml_parser import parse_xml

import os
from lxml import etree

NAME = "DBLP_HARVESTER"


class DblpHarvester(IHarvest):

    def __init__(self, celery=False, path=None):
        # mainly for testing
        if path is not None:
            self.HARVESTER_PATH = path
        # call constructor of base class for initiating values
        IHarvest.__init__(self, NAME, celery)

        # get config values
        try:
            self.xml_path = self.configValues["xml_path"]
            self.dtd_path = self.configValues["dtd_path"]
            self.tags = self.configValues["tags"]
            self.table_name = self.configValues["table_name"]
        except KeyError as e:
            self.logger.critical("Config value %s missing", e)
            raise IHarvest_Exception("Error: config value {} not found".format(e))

        # convert tags to tuple
        self.tags = tuple(self.tags.split(","))

    def init(self):
        # create database if not available
        if self.connector.createTable(self.table_name, DBLP_ARTICLE):
            self.logger.info("Table %s created", self.table_name)
            return True
        else:
            self.logger.critical("Table could not be created")
            return False

    # time_begin and time_end are always valid datetime objects
    def run(self, time_begin=None, time_end=None):
        return parse_xml(self.xml_path, self.dtd_path, self.connector, self.logger, self.tags, time_begin, time_end)



