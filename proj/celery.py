from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab

# start celery and give a name
app = Celery('proj')
#import config from config file
app.config_from_object('celeryconfig')

if __name__ == '__main__':
    app.start()

