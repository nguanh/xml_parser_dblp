# config file for Celery Daemon
from celery.schedules import crontab
from proj import tasks

# default RabbitMQ broker
broker_url = 'amqp://'

# default RabbitMQ backend
#backend liefert ergebnisse unserer asynchronen tasks
#amqp ist das rabbitmq protokoll
#result_backend = 'amqp://'
# use mysql to store results
result_backend = 'db+mysql+mysqlconnector://root:master@localhost/dblp'

# List of modules to import when the Celery worker starts.
imports =('proj.tasks',)

#Schedule of tasks to be executed
beat_schedule={
    'add-every-60-seconds': {
        'task': 'proj.tasks.parse_dblp',
        'schedule': 60.0,
        #'args': (16, 16)
    },

}

#start with celery worker -A proj -l info --beat