from datetime import datetime

from models.scan_status import ScanStatus


class Scan:
    def __init__(self, scan_id):
        self.__id = scan_id
        self.__state = ScanStatus.ACCEPTED
        self.__created_at = datetime.now()
        self.__updated_at = None

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, new_state):
        self.__state = new_state

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    def as_dict(self):
        return {
            'id': self.__id,
            'state': self.__state,
            'created_at': self.__created_at,
            'updated_at': self.__updated_at
        }

    def __str__(self):
        return (
            f'Scan: '
            f'id = {self.__id}, '
            f'state = {self.__state}, '
            f'created_at = {self.__created_at},'
            f'updated_at = {self.__updated_at}'
        )

    def __repr__(self):
        return self.__str__()
