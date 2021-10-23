from flask_apscheduler import APScheduler
import random

from providers.scan import get_not_complete_scans, update_scan
from models.scan_status import ScanStatus
from services.config import ConfigService
from services.logger import LoggerService

logger = LoggerService().logger
config = ConfigService().config
scheduler = APScheduler()

process_rate_in_sec = config['process_rate_in_sec']


def start_process_job():
    try:
        scheduler.add_job(id="process_scans", func=process_scans, trigger='interval', seconds=process_rate_in_sec)
        scheduler.start()
    except Exception as error:
        logger.error(f'Process / Job scheduler | Failed | '
                     f'Error: type = {error.__class__.__name__}, message = {error}')


def process_scans():
    """
    The process system go throw each scan and update their status in the DB

    Assignment assumptions:
    1. For the assignment purpose the status will update randomly
    2. If the status is COMPLETE the scan will not be updated
    """
    logger.info(f'Process / process scans | start')
    try:
        print(f'##### Start update scans state job #####')
        logger.debug(f'Process / process scans | Calling scan provider - get not completed scans')
        scans = get_not_complete_scans()
        logger.debug(f'Process / process scans | Response from get not complete scans| scans = {scans}')
        if scans is not None:
            for scan in scans:
                update_scan_status(scan)
        logger.debug(f'Process / process scans | Response from scan provider - get not completed scans')
    except Exception as error:
        logger.error(
            f'Process / process scans | Ended with failure |'
            f'Error: type = {error.__class__.__name__}, message = {error}')
    else:
        logger.info(f'Process / process scans | Ended successfully')
    finally:
        print(f'##### End update scans state job #####')


def update_scan_status(scan):
    logger.info(f'Process / update scan status | start | scan = {scan}')
    new_state = random.choice(list(ScanStatus))
    print(f'Update scan to: scan id = {scan[0]}, old state = {scan[1]}, new state = {new_state.name}')
    update_scan(scan[0], new_state.name, scan[2])
