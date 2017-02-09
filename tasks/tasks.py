from __future__ import absolute_import, unicode_literals
from .celery import app
from logs.config import LOG_CONFIG
from celery.utils.log import get_task_logger
import logging.config
import logging

from harvester.exception import IHarvest_Exception
from harvester.IHarvester import IHarvest
from celery.exceptions import Ignore
from celery import states

logger = get_task_logger(__name__)
logging.config.dictConfig(LOG_CONFIG)


#TODO test
#TODO parameters as dict
@app.task
def harvest_source(package, className,parameters):
    # import class from parameters
    # TODO try catch
    mod = __import__(package, fromlist=[className])
    klass = getattr(mod, className)
    try:
        source = klass(parameters)
        if isinstance(source, IHarvest) is False:
            raise IHarvest_Exception
        if source.init():
            result = source.run()
            harvest_source.update_state(
                state=states.SUCCESS,
                meta=''
            )

        else:
            harvest_source.update_state(
                state=states.FAILURE,
                meta='Init failed'
            )
    except IHarvest_Exception as e:
        harvest_source.update_state(
            state=states.FAILURE,
            meta=e
        )
    raise Ignore()