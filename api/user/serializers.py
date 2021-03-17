from api.restplus import api
from flask_restplus import fields

create_user_args = api.model('Data to create user', {
    "email": fields.String(description="Email of the user"),
    "fullName": fields.String(description="Name of the user")
})
