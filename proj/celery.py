from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from .tasks import *

# start celery and give a name
app = Celery('proj')
#import config from config file
app.config_from_object('celeryconfig')

'''
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),

    )
'''
if __name__ == '__main__':
    app.start()

#TODO periodic tasks in config verlegen

@app.task
def test(arg):
    print("FANKAR")
    with open('workfile.txt', 'a') as f:
        f.write(arg)
    return "GRAMMAR"