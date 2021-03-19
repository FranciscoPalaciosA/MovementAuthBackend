import logging

from api.restplus import api
from api.user.business.users import (create_user, does_user_exist,
                                    is_login_allowed)
from api.user.serializers import create_user_args, user_args, login_user_args
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

@ns.route('/check_exists')
class UserCollectionCheckExists(Resource):
    @api.expect(user_args, validate=True)
    @api.response(400, 'Error getting user')
    @api.response(200, 'Success.')
    def post(self):
        """
        Creates a user in the db and returns it secret key 
        """
        exists = does_user_exist(request.json)
        return exists


@ns.route('/login')
class UserCollectionLogin(Resource):
    @api.expect(login_user_args, validate=True)
    @api.response(400, 'Error getting user')
    @api.response(200, 'Success.')
    def post(self):
        """
        Endpoint to validate the user's otp
        """
        login = is_login_allowed(request.json)
        return login
