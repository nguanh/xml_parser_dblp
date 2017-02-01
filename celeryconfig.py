# config file for Celery Daemon

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
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'add-every-10-seconds': {
        'task': 'tasks.test',
        'schedule': 10.0,
        'args': ("Hello",)
    },
}