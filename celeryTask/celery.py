from __future__ import absolute_import

from celery import Celery


#DAEMON wird vom pfad / aus gestartet, daher sind alle pfade auch so relativ
# instantiate Celery object
celery = Celery(include=[
    'examples.celery_test'
])

# import celery config file
celery.config_from_object('celeryconfig')

if __name__ == '__main__':
    celery.start()