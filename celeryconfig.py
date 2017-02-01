# config file for Celery Daemon

# default RabbitMQ broker
BROKER_URL = 'amqp://'

# default RabbitMQ backend
CELERY_RESULT_BACKEND = 'amqp://'
#backend liefert ergebnisse unserer asynchronen tasks
#amqp ist das rabbitmq protokoll