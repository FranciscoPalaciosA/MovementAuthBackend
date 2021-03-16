import logging
import traceback
from datetime import datetime

from flask_restplus import Api
from api import settings

log = logging.getLogger(__name__)

api = Api(prefix='/api/v1', version='1.0', title='MovementAuthBackend',
          description='Backend used by Movement Auth School Project', validate=True)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    logf = open("error.log", "w")
    logf.write("Error occured. {0}: {1}\n".format(str(datetime.now()), str(e)))
    return {'message': message, 'error': str(e)}, 500
