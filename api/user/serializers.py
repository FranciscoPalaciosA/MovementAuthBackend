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
    "userId": fields.String(description="Id of the user"),
    "sequence": fields.String(description="Sequence given to the user"),
    "otp": fields.String(description="OTP from the user"),
})

survey_args = api.model('Arguments to recieve on survey answered', {
    "userId": fields.String(description="Id of the user"),
    "sum": fields.Integer(description="The sum of the answers"),
    "total": fields.Float(description="The total (sum*2.5) of the answers"),
    "question1": fields.Integer(description="Answer to question 1"),
    "question2": fields.Integer(description="Answer to question 2"),
    "question3": fields.Integer(description="Answer to question 3"),
    "question4": fields.Integer(description="Answer to question 4"),
    "question5": fields.Integer(description="Answer to question 5"),
    "question6": fields.Integer(description="Answer to question 6"),
    "question7": fields.Integer(description="Answer to question 7"),
    "question8": fields.Integer(description="Answer to question 8"),
    "question9": fields.Integer(description="Answer to question 9"),
    "question10": fields.Integer(description="Answer to question 10")
})