from __future__ import absolute_import, unicode_literals
from .celery import app
from dblp.xml_parser import parse_xml
from mysqlWrapper.mariadb import  MariaDb
from dblp.queries import DBLP_ARTICLE
from dblp.exception import Dblp_Parsing_Exception

from celery.utils.log import get_task_logger
import logging.config
import logging

logger = get_task_logger(__name__)
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
    },
    'handlers': {
        'tasks.tasks': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/dblp.log',
            'formatter': 'default',
        },
        'dblp.error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/dblp_error.log',
            'formatter': 'default',
        },
    },
    'loggers': {
        'tasks.tasks': {
            'handlers': ['tasks.tasks'],
            'level': 'INFO',
        },
        'dblp.xml_parser': {
            'handlers': ['tasks.tasks','dblp.error'],
            'level': 'INFO',
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)

#TODO set logger setting
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
    except Dblp_Parsing_Exception as err:
        logger.critical(err)
        #TODO set state fail
    except Exception as err:
        print(err)

