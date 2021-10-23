#!/usr/bin/python3

import logging

from server.server import app
from providers.db.sqlite import SqliteService
from services.singleton import SingletonMetaClass
from providers.process import start_process_job
try:
    logging.info('##### At-bay - Cyber Scans System Started #####')
    logging.debug('Run sqlite db...')
    SqliteService()
    logging.debug('Run process job...')
    start_process_job()
    logging.debug('Run server...')
    app.run(debug=True)
    logging.info('##### At-bay - Cyber Scans System Stopped #####')
except KeyError as e:
    SingletonMetaClass.clear()