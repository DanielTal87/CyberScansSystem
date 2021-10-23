import sqlite3

from services.config import ConfigService
from services.logger import LoggerService
from services.singleton import SingletonMetaClass

config = ConfigService().config
logger = LoggerService().logger

QUERY_CREATE_SCANS_TABLE = """
    CREATE TABLE IF NOT EXISTS 
    scans(scan_id TEXT PRIMARY KEY, status TEXT, created_at TEXT, updated_at TEXT)
"""

QUERY_INSERT_SCAN = """
    INSERT OR IGNORE 
    INTO scans VALUES (?, ?, ?, '')
"""

QUERY_GET_SCAN = """
    SELECT *
    FROM scans
    WHERE scan_id = ?
    LIMIT 1
"""

QUERY_UPDATE_SCAN = """
    REPLACE
    INTO scans VALUES (?, ?, ?, ?)
"""

QUERY_GET_ALL_NOT_COMPLETE_SCANS = """
    SELECT *
    FROM scans
    WHERE status != 'COMPLETE'
"""


class SqliteService(metaclass=SingletonMetaClass):
    def __init__(self):
        self.__connection = sqlite3.connect("CSS.db", check_same_thread=False)
        self.__cursor = self.__connection.cursor()
        self.create_tables()

    @property
    def cursor(self):
        return self.__cursor

    def create_tables(self):
        self.__cursor.execute(QUERY_CREATE_SCANS_TABLE)
        self.__connection.commit()

    def inset_scan(self, scan_id, status, created_at):
        self.__cursor.execute(QUERY_INSERT_SCAN, [scan_id, status, created_at])
        self.__connection.commit()

    def get_scan(self, scan_id):
        get_scan = self.__cursor.execute(QUERY_GET_SCAN, [scan_id]).fetchone()
        return get_scan

    def update_scan(self, scan_id, status, created_at, updated_at):
        self.__cursor.execute(QUERY_UPDATE_SCAN, [scan_id, status, created_at, updated_at])
        self.__connection.commit()

    def get_not_complete_scans(self):
        scans = self.__cursor.execute(QUERY_GET_ALL_NOT_COMPLETE_SCANS)
        self.__connection.commit()
        return list(scans)
