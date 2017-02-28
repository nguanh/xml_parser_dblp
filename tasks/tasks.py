from __future__ import absolute_import, unicode_literals
from .celery import app
from celery.utils.log import get_task_logger
import logging.config
import logging

from harvester.exception import IHarvest_Exception,IHarvest_Disabled
from harvester.IHarvester import IHarvest
from celery.exceptions import Ignore
from celery import states
import sys
import os


#logging.config.dictConfig(LOG_CONFIG)


#TODO test
#TODO parameters as dict
@app.task
def harvest_source(package, class_name, name, **parameters):
    """

    :param package: relative path to package
    :param class_name: class name in package
    :param name: name of the harvester (important for config)
    :param parameters: parameters for harvester as dict parameters
    :return:
    """
    # init logger, generate logger for every tasks
    logger = get_task_logger(name)
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("{}.log".format(name))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)

    try:
        # add path to system
        file_path = os.path.realpath(__file__)
        project_path = os.path.dirname(os.path.dirname(file_path))
        sys.path.append(project_path)
        # import class from parameters
        mod = __import__(package, fromlist=[class_name])
        imported_class = getattr(mod, class_name)
    except ImportError as e:
        logger.error(e)
        harvest_source.update_state(
            state=states.FAILURE,
            meta=e,
        )
        raise Ignore()
    try:
        source = imported_class(logger, name, **parameters)
        if isinstance(source, IHarvest) is False:
            raise IHarvest_Exception(class_name + " is not an instance of IHarvest")
        if source.init():
            print("Starting", name)
            logger.info("Starting Task %s", name)
            result = source.run()
            print("Finishing", name)
            logger.info("Finished Task %s", name)
            harvest_source.update_state(
                state=states.SUCCESS,
                meta=''
            )
        else:
            logger.error("Initialization of %s failed", name)
            harvest_source.update_state(
                state=states.FAILURE,
                meta='Init failed'
            )
    except IHarvest_Exception as e:
        logger.critical(e)
        harvest_source.update_state(
            state=states.FAILURE,
            meta=e
        )
    except IHarvest_Disabled:
        # task is disabled
        print("Skipping Task", name)
        logger.info("Task %s is disabled and skipped", name);
        harvest_source.update_state(
            state=states.SUCCESS,
            meta=''
        )
    raise Ignore()
