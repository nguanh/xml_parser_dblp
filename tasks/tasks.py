from __future__ import absolute_import, unicode_literals
from .celery import app
from mysqlWrapper.mariadb import  MariaDb
from oai.oaimph_parser import harvestOAI
from oai.queries import OAI_DATASET
from logs.config import LOG_CONFIG
from celery.utils.log import get_task_logger
import logging.config
import logging

from harvester.exception import IHarvest_Exception
from dblp.dblpharvester import DblpHarvester
from celery.exceptions import Ignore
from celery import states

logger = get_task_logger(__name__)
logging.config.dictConfig(LOG_CONFIG)

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
#TODO pass any object

@app.task
def harvest_source():

    try:
        source = DblpHarvester()
        if source.init():
            result = source.run()
            harvest_source.update_state(
                state=states.FAILURE,
                meta='REASON FOR FAILURE'
            )
        else:
            pass
    except IHarvest_Exception as e:
        print(e)
        pass

    raise Ignore()