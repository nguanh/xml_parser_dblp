from __future__ import absolute_import, unicode_literals
from .celery import app
from harvester.exception import IHarvest_Exception, IHarvest_Disabled
from celery.exceptions import Ignore
from celery import states
from .harvest_task import harvest_task

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
    try:
        harvest_task(package, class_name, name,None , parameters)
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