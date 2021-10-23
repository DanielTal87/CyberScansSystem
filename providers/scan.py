from datetime import datetime

from models.scan import Scan
from providers.db.sqlite import SqliteService
from services.logger import LoggerService

logger = LoggerService().logger
db = SqliteService()


def create_scan(scan_id):
    logger.info(f'Providers / scan / create scan - start')
    try:
        scan = Scan(scan_id)
        logger.debug(f'Providers / scan / create scan | Calling to insert scan to DB | input = {scan}')
        db.inset_scan(str(scan.id), str(scan.state.name), str(scan.created_at))
        logger.debug(f'Providers / scan / create scan | Insert scan to DB ended successfully')
    except Exception as error:
        logger.error(f'Providers / scan / create scan | - Ended with failure | '
                     f'Error: type = {error.__class__.__name__}, message = {error}')
        raise f'Create scan failed - error = {error}'
    else:
        logger.info(f'Providers / scan / create scan | - Ended successfully')
        return scan


def get_scan_status(scan_id):
    logger.info(f'Providers / scan / get scan status - start')
    try:
        logger.debug(f'Providers / scan / get scan status | Calling to get scan from DB | scan_id = {scan_id}')
        scan = db.get_scan(str(scan_id))
        logger.debug(f'Providers / scan / get scan status | Getting scan from DB ended successfully | scan = {scan}')
    except Exception as error:
        logger.error(f'Providers / scan / get scan status | Ended with failure | '
                     f'Error: type = {error.__class__.__name__}, message = {error}')
        raise f'Get scan status failed - error = {error}'
    else:
        logger.info(f'Providers / scan / get scan status | Ended successfully')
        if scan is None:
            return None
        return scan[1]


def get_not_complete_scans():
    logger.info(f'Providers / scan / get not ended scans - start')
    try:
        logger.debug(f'Providers / scan / get not ended scans | Calling to get not ended scans from DB')
        scans = db.get_not_complete_scans()
        logger.debug(f'Providers / scan / get not ended scans | Getting not ended scans from DB ended successfully')
    except Exception as error:
        logger.error(f'Providers / scan / get not ended scans | Ended with failure | '
                     f'Error: type = {error.__class__.__name__}, message = {error}')
        raise f'Get scan status failed - error = {error}'
    else:
        logger.info(f'Providers / scan / get not ended scans | Ended successfully')
        return scans


def update_scan(scan_id, state, created_at):
    logger.info(f'Providers / scan / update scan - start | scan id = {scan_id}, state = {state}')
    try:
        logger.debug(f'Providers / scan / update scan | Calling update scan in DB')
        scans = db.update_scan(scan_id, state, created_at, str(datetime.now()))
        logger.debug(f'Providers / scan / update scan | Updating scans ended successfully')
    except Exception as error:
        logger.error(f'Providers / scan / update scan | Ended with failure | '
                     f'Error: type = {error.__class__.__name__}, message = {error}')
        raise f'Update scan status failed - error = {error}'
    else:
        logger.info(f'Providers / scan / update scan | Ended successfully')
        return scans
