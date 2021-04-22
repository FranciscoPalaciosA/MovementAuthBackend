import logging

from api.utils.fire import get_reference
from api.utils.totp import generate_seed, generate_secret_key, get_totp_token

import uuid

def create_user(args):
    if does_user_exist(args["email"]):
        return ""
    
    seed = generate_seed()
    secret = generate_secret_key(seed)
    user = {
        'email': args["email"], 
        'name': args["fullName"],
        'secret': secret
    }
    u_id = uuid.uuid4()
    ref = get_reference(f'users/{u_id}')
    ref.set(user)
    return f'email:{args["email"]}-secret:{secret}'

def does_user_exist(email_to_check):
    users = get_reference('users').get()
    for attr, value in users.items():
        if value['email'] == email_to_check['email']:
            return attr
    return False

def is_login_allowed(json):
    u_id = json['userId']
    user_key = get_user_key(u_id)
    if user_key == None:
        return False
    sequence = json['sequence']
    print("sequence = ", sequence)
    logging.info("sequence = ", sequence)
    otp = json['otp']
    correct_otps = get_totp_token(user_key, sequence.split(','))
    print("Correct otp = ", correct_otps)
    logging.info("Correct otp = ", correct_otps)
    return otp in correct_otps

def get_user_key(u_id):
    user = get_reference(f'users/{u_id}').get()
    if user is None: return None
    else:
        return user['secret']

def save_results(json):
    status = True
    try:
        user_survey = get_reference(f'users/{json["userId"]}/survey')
        if user_survey.get() is not None:
            json.pop('userId', None)
            user_survey.update(json)
        else:
            status = False
    except Exception as e:
        status = False
    return status