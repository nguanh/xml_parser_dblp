# config file for Celery Daemon
from celery.schedules import crontab
# default RabbitMQ broker
broker_url = 'amqp://'

# default RabbitMQ backend
# backend liefert ergebnisse unserer asynchronen tasks
# amqp ist das rabbitmq protokoll
# result_backend = 'amqp://'
# use mysql to store results
result_backend = 'db+mysql+mysqlconnector://root:master@localhost/dblp'

# List of modules to import when the Celery worker starts.
imports = ('tasks.tasks',)


# Schedule of tasks to be executed
beat_schedule = {
    'dblp-harvester': {
        'task': 'tasks.tasks.harvest_source',
        'schedule': 300,
        'args': ("dblp.dblpharvester", "DblpHarvester", "DBLP_HARVESTER")
    },
    'oai-harvester': {
        'task': 'tasks.tasks.harvest_source',
        'schedule': 300,
        'args': ("oai.oaiharvester", "OaiHarvester", "OAI_HARVESTER")
    },
    'arxiv-harvester': {
        'task': 'tasks.tasks.harvest_source',
        'schedule': 60,
        'args': ("oai.arxivharvester", "ArXivHarvester", "ARXIV_HARVESTE")
    }
}
# start with tasks worker -A tasks -l info --beat
# 'schedule': crontab(minute=10, hour=2),
