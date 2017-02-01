# config file for Celery Daemon

# default RabbitMQ broker
broker_url = 'amqp://'

# default RabbitMQ backend
#result_backend = 'amqp://'
result_backend = 'db+mysql+mysqlconnector://root:master@localhost/dblp'

# List of modules to import when the Celery worker starts.
imports =('proj.tasks',)
#backend liefert ergebnisse unserer asynchronen tasks
#amqp ist das rabbitmq protokoll