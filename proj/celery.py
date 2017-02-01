from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab

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
# Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )
'''
if __name__ == '__main__':
    app.start()


# TODO
# import celery config file

