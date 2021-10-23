from enum import Enum, auto


class ScanStatus(Enum):
    """
    Accepted – the request for a new scan has been received and is pending processing
    Running – the scan is currently running
    Error – an error occurred during the scan (e.g. bad domain name)
    Complete – the scan was completed successfully
    Not-Found – the scan-id could not be found
    """
    ACCEPTED = auto()
    RUNNING = auto()
    ERROR = auto()
    COMPLETE = auto()
    NOT_FOUND = auto()

    @classmethod
    def from_str(cls, name):
        for status, status_name in ScanStatus.items():
            if status_name == name:
                return status
        raise ValueError(f'The status {name} is invalid')

    def to_name(self):
        return ScanStatus[self.value]

    def equals(self, string):
        return self.name == string
