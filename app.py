import json
import logging
import os

from flask import Flask, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from api.restplus import api
from api.user.endpoints.users import ns as users_namespace

app = Flask(__name__)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)
api.init_app(app)

api.add_namespace(users_namespace)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',
            port=int(os.environ.get('PORT', 8000)))

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.handlers.extend(gunicorn_logger.handlers)
    app.logger.debug('this will show in the log')
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
