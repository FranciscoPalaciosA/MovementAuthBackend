from api.restplus import api
from flask_restplus import fields

upload_mov_args = api.model('Data to upload user', {
    "movement": fields.String(description="Name of movement"),
})
