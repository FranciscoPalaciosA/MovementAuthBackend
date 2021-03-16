import logging

from api.restplus import api
from api.user.business.users import (create_user)
from api.user.serializers import create_user_args
from flask import abort, request
from flask_restplus import Resource

log = logging.getLogger(__name__)

ns = api.namespace(
    'users', description='Operations related to users')


@ns.route('/')
class UsersCollection(Resource):
    @api.expect(create_user_args, validate=True)
    @api.response(400, 'Error creating user')
    @api.response(200, 'Success.')
    def post(self):
        """
        Creates a user in the db and returns it secret key 
        """
        string_for_qr = create_user(request.json)
        if string_for_qr != "":
            return string_for_qr
        else:
            abort(400, 'Error creating user')
