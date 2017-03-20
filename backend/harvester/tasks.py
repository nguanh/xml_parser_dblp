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


@shared_task()
def printyy(a,b):
    print(a,b)


@shared_task
def add(x, y):
    print(str(x+y))
    return x + y

'''
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
'''