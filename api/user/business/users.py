import logging
from datetime import datetime 
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
    return f'email:{args["email"]}?secret:{secret}?uid:{u_id}'

def does_user_exist(email_to_check):
    users = get_reference('users').get()
    for attr, value in users.items():
        if value['email'] == email_to_check:
            return attr
    return False

def is_login_allowed(json):
    u_id = json['userId']
    user_key = get_user_key(u_id)
    if user_key == None:
        return False
    sequence = json['sequence']

    otp = json['otp']
    correct_otps = get_totp_token(user_key, sequence.split(','))

    login_allowed = otp in correct_otps
    register_attempt(login_allowed, u_id)

    logging.info("sequence sent = ", sequence)
    logging.info("Correct otp = ", correct_otps)

    return login_allowed

def get_user_key(u_id):
    user = get_reference(f'users/{u_id}').get()
    if user is None: return None
    else:
        return user['secret']

def save_results(json):
    status = True
    try:
        user_survey = get_reference(f'users/{json["userId"]}/survey')
        json.pop('userId', None)
        user_survey.set(json)
    except Exception as e:
        status = False
    return status

def register_attempt(login_allowed, u_id):
    if login_allowed:
        path = 'attempts/success'
    else:
        path = 'attempts/failed'
    attempt_ref = get_reference(f'users/{u_id}/' + path)
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    attempt_ref.push({'time': timestamp})
    