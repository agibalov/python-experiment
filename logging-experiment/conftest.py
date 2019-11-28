import logging
import logging.config
from importlib import reload

import pytest


@pytest.fixture(scope='function', autouse=True)
def init_logging():
    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'class': 'basic_test.ExtraAppendingFormatter',
                'stream': 'ext://sys.stdout',
                'format': '%(asctime)s %(levelname)-8s %(processName)-5s %(threadName)-5s %(name)-12s %(message)s <%(extra_str)s>'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': [
                'console'
            ]
        }
    })
    yield
    reload(logging)
