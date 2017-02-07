from harvester.IHarvester import IHarvest
from harvester.exception import IHarvest_Exception

from dblp.queries import DBLP_ARTICLE, ADD_DBLP_ARTICLE
from dblp.exception import Dblp_Parsing_Exception
from dblp.helper import parse_mdate, parse_year, dict_to_tuple, parse_title

import os
from lxml import etree


class DblpHarvester(IHarvest):
    # TODO test

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
        if self.connector.createTable(self.table_name, DBLP_ARTICLE):
            self.logger.info("Table %s created", self.table_name)
            return True
        else:
            self.logger.critical("Table could not be created")
            return False

    # time_begin and time_end are always valid datetime objects
    def run(self, time_begin=None, time_end=None):

        if os.path.isfile(self.xml_path) is False:
            raise Dblp_Parsing_Exception("Invalid XML path")
        if os.path.isfile(self.xml_path) is False:
            raise Dblp_Parsing_Exception("Invalid DTD path")

        # init values
        success_count = 0
        overall_count = 0
        etree.DTD(file=self.dtd_path)

        time_range = time_begin is not None and time_end is not None
        self.connector.set_query(ADD_DBLP_ARTICLE)

        for event, element in etree.iterparse(self.xml_path, tag=self.tags, load_dtd=True):

            overall_count += 1
            dataset = {
                'key': element.get('key'),
                'mdate': parse_mdate(element.get('mdate')),
                'title': ''
            }

            # check date range
            if time_range:
                if (time_begin <= dataset["mdate"] <= time_end) is False:
                    continue

            author_csv_list = ''

            # iterate through elements of block
            for child in element:
                if child.tag == 'author':
                    # stores authors as csv
                    author_csv_list += child.text + ";"
                elif child.tag == 'year':
                    dataset[child.tag] = parse_year(child.text)
                elif child.tag == 'title':
                    title = parse_title(child).replace('\n', '')
                    dataset[child.tag] = title
                else:
                    dataset[child.tag] = str(child.text).strip()

            dataset['author'] = author_csv_list
            tup = dict_to_tuple(dataset)

            try:
                self.connector.execute(tup)
            except Exception as e:
                self.logger.error("MariaDB error: %s", e)
            else:
                success_count += 1
                self.logger.info("%s: %s", success_count, element.get('key'))
            element.clear()

            if overall_count > 100:
                return 101

        self.logger.info("Final Count : %s", success_count)
        self.connector.close_connection()
        return success_count
