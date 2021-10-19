#!/usr/bin/python3

import datetime
import logging

from services.singleton import SingletonMetaClass


class LoggerService(metaclass=SingletonMetaClass):
    def __init__(self):
        self.logger = logging.getLogger("Cyber Scans System")
        logging.basicConfig(filename=f'logs/CSS-{datetime.date.today()}.log',
                            format='%(asctime)s | %(levelname)s | %(message)s',
                            level=logging.DEBUG)
