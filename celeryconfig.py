# config file for Celery Daemon
from celery.schedules import crontab
from dblp.dblpharvester import DblpHarvester
# default RabbitMQ broker
broker_url = 'amqp://'

# default RabbitMQ backend
#backend liefert ergebnisse unserer asynchronen tasks
#amqp ist das rabbitmq protokoll
#result_backend = 'amqp://'
# use mysql to store results
result_backend = 'db+mysql+mysqlconnector://root:master@localhost/dblp'

# List of modules to import when the Celery worker starts.
imports =('tasks.tasks',)


#Schedule of tasks to be executed
beat_schedule={
    'add-every-60-seconds': {
        'task': 'tasks.tasks.parse_dblp',
        'schedule': crontab(minute=10, hour=2),
        #'args': (16, 16)
    },
    'generic-task': {
        'task': 'tasks.tasks.harvest_source',
        'schedule': 30,
        'args': (DblpHarvester, 16)
    },


}

#TODO results integrieren FAIL/PENDING usw
#start with tasks worker -A tasks -l info --beat