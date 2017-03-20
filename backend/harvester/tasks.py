# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.exceptions import Ignore
from celery import states
from .exception import IHarvest_Disabled,IHarvest_Exception
from .harvest_task import harvest_task


@shared_task()
def test():
    print ("Hello")


@shared_task
def harvest(package, class_name, name):
    """

    :param package: relative path to package
    :param class_name: class name in package
    :param name: name of the harvester (important for config)
    :param parameters: parameters for harvester as dict parameters
    :return:
    """
    print(package)
    '''

    try:
       # harvest_task(package, class_name, name, None)
        print("hello")
    except ImportError as e:
        harvest.update_state(
            state=states.FAILURE,
            meta=e,
        )
        raise Ignore()
    except IHarvest_Exception as e:
        harvest.update_state(
            state=states.FAILURE,
            meta=e
        )
    except IHarvest_Disabled:
        # task is disabled
        harvest.update_state(
            state=states.SUCCESS,
            meta=''
        )
    '''