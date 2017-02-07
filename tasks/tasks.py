from __future__ import absolute_import, unicode_literals
from .celery import app
from dblp.xml_parser import parse_xml
from mysqlWrapper.mariadb import  MariaDb
from dblp.queries import DBLP_ARTICLE
from dblp.exception import IHarvest_Exception
from oai.oaimph_parser import harvestOAI
from oai.queries import OAI_DATASET
from logs.config import LOG_CONFIG
from celery.utils.log import get_task_logger
import logging.config
import logging

from harvester.exception import IHarvest_Exception
from dblp.dblpharvester import DblpHarvester

logger = get_task_logger(__name__)
logging.config.dictConfig(LOG_CONFIG)

@app.task
def parse_dblp():
    xml_path = "/home/nguyen/raw_file/dblp.xml"
    dtd_path ="/home/nguyen/raw_file/dblp.dtd"
    credentials = {
        'user': 'root',
        'password': 'master',
        'host': '127.0.0.1',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_general_ci'
    }
    DB_NAME="harvester"
    DBLP_TABLE_NAME = "dblp_article"

    try:
        database = MariaDb(credentials)
        #create db and table, if not existing
        database.create_db(DB_NAME)
        database.createTable(DBLP_TABLE_NAME, DBLP_ARTICLE)
        x = parse_xml(xml_path, dtd_path, database, ("article", "inproceedings"), celery=True)
    except IHarvest_Exception as err:
        logger.critical(err)
        #TODO set state fail
    except Exception as err:
        print(err)


@app.task
def parse_oai_pmh():
    credentials = {
        'user': 'root',
        'password': 'master',
        'host': '127.0.0.1',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_general_ci'
    }
    DB_NAME="harvester"
    OAI_TABLE_NAME = "oai_articles"
    link = 'http://citeseerx.ist.psu.edu/oai2'
    try:
        database = MariaDb(credentials)
        database.create_db(DB_NAME)

        database.createTable(OAI_TABLE_NAME, OAI_DATASET)
        x = harvestOAI(link, database, celery=True)
    except IHarvest_Exception as err:
        logger.critical(err)
    except Exception as err:
        print(err)

#TODO set state fail
#TODO check instance
@app.task
def harvest_source():
    try:
        source = DblpHarvester()
        if source.init():
            result = source.run()
    except IHarvest_Exception as e:
        pass