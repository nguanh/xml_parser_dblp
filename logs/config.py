LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
    },
    'handlers': {
        'dblp': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/dblp.log',
            'formatter': 'default',
        },
        'oai': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/oai.log',
            'formatter': 'default',
        },

    },
    'loggers': {

        'DBLP_HARVESTER': {
            'handlers': ['dblp'],
            'level': 'INFO',
        },

        'OAI_HARVESTER': {
            'handlers': ['oai'],
            'level': 'INFO',
        },
    }
}
