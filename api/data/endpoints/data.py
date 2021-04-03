import logging

from api.restplus import api
from api.data.business.data import (upload_movement, check_movement)
from api.data.serializers import upload_mov_args
from flask import abort, request
from flask_restplus import Resource

log = logging.getLogger(__name__)

ns = api.namespace(
    'data', description='Operations related to data')


@ns.route('/')
class DataCollection(Resource):
    @api.expect(upload_mov_args, validate=False)
    @api.response(400, 'Error uploading data')
    @api.response(200, 'Success.')
    def post(self):
        """
        Uploads the data for a movement patter to firebase
        """
        status = upload_movement(request.json)
        if status:
            return status
        else:
            abort(400, 'Error uploading data')

@ns.route('/check-movement')
class DataCheckCollection(Resource):
    @api.expect(upload_mov_args, validate=False)
    @api.response(400, 'Error uploading data')
    @api.response(200, 'Success.')
    def post(self):
        """
        Uploads the data for a movement patter to firebase
        """
        return check_movement(request.json)
