from .oaiharvester import OaiHarvester
from .queries import ARXIV_ARTICLE, ADD_ARXIV
from .oaimph_parser import harvestOAI
from .arxiv_handler import ArXivRecord, parse_arxiv


class ArXivHarvester(OaiHarvester):

    def __init__(self, logger, name, path=None):
        # call constructor of base class for initiating values
        OaiHarvester.__init__(self, logger, name, path)

    def init(self):
        # create database if not available
        if self.connector.createTable(self.table_name, ARXIV_ARTICLE):
            self.logger.info("Table %s created", self.table_name)
            return True
        else:
            self.logger.critical("Table could not be created")
            return False

    # time_begin and time_end are always valid datetime objects
    def run(self, time_begin=None, time_end=None):
        return harvestOAI(self.link, self.connector, self.logger,
                          processing_function=parse_arxiv, xml_format="arXiv",
                          query=ADD_ARXIV, parsing_class=ArXivRecord,
                          startDate=time_begin, endDate=time_end, limit=self.limit)

