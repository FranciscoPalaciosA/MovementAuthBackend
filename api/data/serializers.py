from api.restplus import api
from flask_restplus import fields

upload_mov_args = api.model('Data to upload user', {
    "movement": fields.String(description="Name of movement"),
})

time_seq_args = api.model('Args to time the sequence request', {
    "miliseconds": fields.Float(description="Miliseconds"),
})
