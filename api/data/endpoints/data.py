import logging

from api.restplus import api
from api.data.business.data import (upload_movement, check_movement, 
                                    convert_to_sequence, time_sequence,
                                    improved_check_movement,
                                    improved_get_sequence)
from api.data.serializers import upload_mov_args, time_seq_args
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

@ns.route('/improved_model')
class ImprovedModelCollection(Resource):
    @api.expect(upload_mov_args, validate=False)
    @api.response(400, 'Error with data')
    @api.response(200, 'Success')
    def post(self):
        return improved_check_movement(request.json)


@ns.route('/check-movement')
class DataCheckCollection(Resource):
    @api.expect(upload_mov_args, validate=False)
    @api.response(400, 'Error uploading data')
    @api.response(200, 'Success.')
    def post(self):
        """
        Checks if a movement is what it's supposed to be.
        """
        return check_movement(request.json)


@ns.route('/get-sequence')
class MovementConversionCollection(Resource):
    @api.expect(upload_mov_args, validate=False)
    @api.response(400, 'Error uploading data')
    @api.response(200, 'Success.')
    def post(self):
        """
        Returns the sequence of strings to replace
        """
        #return convert_to_sequence(request.json)
        return improved_get_sequence(request.json)


@ns.route('/time-sequence')
class TimingSequence(Resource):
    @api.expect(time_seq_args, validate=True)
    @api.response(400, 'Error uploading data')
    @api.response(200, 'Success.')
    def post(self):
        """
        Saves the miliseconds it took to get the sequence
        """
        return time_sequence(request.json)
