LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
    },
    'handlers': {
        'tasks.tasks': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/dblp.log',
            'formatter': 'default',
        },
        'dblp.error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/dblp_error.log',
            'formatter': 'default',
        },
        'oai.error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/oai_error.log',
            'formatter': 'default',
        },
    },
    'loggers': {
        'tasks.tasks': {
            'handlers': ['tasks.tasks'],
            'level': 'INFO',
        },
        'dblp.xml_parser': {
            'handlers': ['tasks.tasks','dblp.error'],
            'level': 'INFO',
        },
        'oai.harvestOAI': {
            'handlers': ['oai.error'],
            'level': 'INFO',
        },
        'DBLP_HARVESTER': {
            'handlers': ['tasks.tasks','dblp.error'],
            'level': 'INFO',
        },
    }
}
