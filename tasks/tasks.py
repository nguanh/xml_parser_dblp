from __future__ import absolute_import, unicode_literals
from .celery import app
from harvester.exception import IHarvest_Exception, IHarvest_Disabled
from pub_storage.exception import IIngester_Exception,IIngester_Disabled
from celery.exceptions import Ignore
from celery import states
from .harvest_task import harvest_task
from .ingest_task import ingest_task

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

@app.task
def ingest_source(package, class_name, **parameters):
    try:
        ingest_task(package, class_name, None)
    except ImportError as e:
        ingest_source.update_state(
            state=states.FAILURE,
            meta=e,
        )
        raise Ignore()
    except IIngester_Exception as e:
        ingest_source.update_state(
            state=states.FAILURE,
            meta=e
        )
    except IIngester_Disabled:
        # task is disabled
        ingest_source.update_state(
            state=states.SUCCESS,
            meta=''
        )