# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import Ignore
from celery import states
from .exception import IHarvest_Disabled,IHarvest_Exception
from .harvest_task import harvest_task

from celery.utils.log import get_task_logger
import logging
@shared_task
def add(x, y):
    return x + y


@shared_task
def printtest(package, class_name, name, **parameters):
    # init logger, generate logger for every tasks
    logger = get_task_logger("hallo")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("{}.log".format(name))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    print("HALLLLOOO")
    logger.info("Funktioniert es?")

@shared_task
def print_par(package, class_name, name):
    print(package,class_name,name)

@shared_task
def harvest_source(package, class_name, name, **parameters):
    """

    :param package: relative path to package
    :param class_name: class name in package
    :param name: name of the harvester (important for config)
    :param parameters: parameters for harvester as dict parameters
    :return:
    """
    try:
        harvest_task(package, class_name, name, None)
    except ImportError as e:
        harvest_source.update_state(
            state=states.FAILURE,
            meta=e,
        )
        raise Ignore()
    except IHarvest_Exception as e:
        harvest_source.update_state(
            state=states.FAILURE,
            meta=e
        )
    except IHarvest_Disabled:
        # task is disabled
        harvest_source.update_state(
            state=states.SUCCESS,
            meta=''
        )
