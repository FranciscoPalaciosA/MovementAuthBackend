from api.restplus import api
from flask_restplus import fields

create_user_args = api.model('Data to create user', {
    "email": fields.String(description="Email of the user"),
    "fullName": fields.String(description="Name of the user")
})

user_args = api.model('User email', {
    "email": fields.String(description="Email of the user"),
})

login_user_args = api.model('Arguments to login user', {
    "userId": fields.String(description="Email of the user"),
    "sequence": fields.String(description="Sequence given to the user"),
    "otp": fields.String(description="OTP from the user"),
})