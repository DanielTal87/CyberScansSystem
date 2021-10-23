from uuid import uuid4

from flask import Flask
from flask_restful import Api, Resource
from redis import Redis
from rq import Queue

from providers.health_check import random_health_check
from providers.scan import create_scan, get_scan_status
from services.logger import LoggerService

logger = LoggerService().logger
app = Flask(__name__)
api = Api(app)
tasks_queue = Queue(connection=Redis())


class HealthCheck(Resource):
    def get(self):
        """
        Checking if the service is alive.
        For the assignment the API may return a failure
        :return: True/False randomly
        """
        logger.info(f'Server / HealthCheck | start')
        try:
            random_health_check()
        except Exception as error:
            logger.error(
                f'Server / HealthCheck | failed with an error: type = {error.__class__.__name__}, message = {error}')
            return {'message': "Health check failed"}, 503
        else:
            logger.info(f'CSS / HealthCheck | Ended successfully')
            return {'message': "It's Alive, It's Alive..."}, 200


class Ingest(Resource):
    def post(self):
        """
        Create a new cyber scan
        :return: Scan id
        """
        logger.info(f'Ingest / post | Start')
        try:
            scan_id = str(uuid4())[:8]
            logger.debug(f'Ingest / post | Adding create scan task to the tasks queue | scan_id = {scan_id}')
            tasks_queue.enqueue(create_scan, scan_id)
            logger.debug(f'Ingest / post | '
                         f'Insert create scan task to the tasks queue ended successfully | scan_id = {scan_id}')
        except Exception as error:
            logger.error(
                f'Ingest / post | Ended with failure | Error: type = {error.__class__.__name__}, message = {error}')
            return {
                       'message': "Ingesting a new scan",
                       'status': 'failed'
                   }, 400
        else:
            logger.info(f'Ingest / post | Ended successfully')
            return {
                       'scan_id': scan_id,
                       'message': "Ingesting a new scan",
                       'status': 'success'
                   }, 201


class Status(Resource):
    """
    Get the status of a scan by scan id
    :param Scan ID - the id of an ingested scan
    :return Scan status
    """
    def get(self, scan_id):
        logger.info(f'Status / get | Start | scan id = {scan_id}')
        try:
            logger.debug(f'Status / get | Calling to provider get scan status | scan_id = {scan_id}')
            status = get_scan_status(scan_id)
            logger.debug(f'Status / get | '
                         f'Getting scan status ended successfully | scan_id = {scan_id}, status = {status}')
            if status is None:
                return {
                           'scan_id': scan_id,
                           'message': "Get scan status",
                           'status': 'Not found'
                       }, 200
        except Exception as error:
            logger.error(
                f'Status / get | Ended with failure | Error: type = {error.__class__.__name__}, message = {error}')
            return {
                       'message': "Get scan status",
                       'status': 'failed'
                   }, 400
        else:
            logger.info(f'Status / get | Ended successfully')
            return {
                       'scan_id': scan_id,
                       'status': status,
                       'message': "Get scan status"
                   }, 200


api.add_resource(HealthCheck, '/health-check')
api.add_resource(Ingest, '/ingest')
api.add_resource(Status, '/status/<string:scan_id>')
