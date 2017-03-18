
from pub_storage.setup_database import setup_database
from pub_storage.constants import DATABASE_NAME
from pub_storage.ingester import ingest_data2
from dblp.dblpingester import DblpIngester
from oai.arxivingester import ArxivIngester
import logging

# init logger, generate logger for every tasks
logger = logging.getLogger("ingester")
logger.setLevel(logging.DEBUG)
# create the logging file handler
fh = logging.FileHandler("{}.log".format("ingester"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add handler to logger object
logger.addHandler(fh)

setup_database(DATABASE_NAME)
mode = 1
if mode == 0:
    ingester = DblpIngester(DATABASE_NAME,"harvester")
else:
    ingester = ArxivIngester(DATABASE_NAME, "harvester")


ingest_data2(ingester, DATABASE_NAME)
