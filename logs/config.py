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

    },
    'loggers': {

        'DBLP_HARVESTER': {
            'handlers': ['dblp'],
            'level': 'INFO',
        },
    }
}
