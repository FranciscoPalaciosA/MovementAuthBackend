from api.utils.fire import get_reference
from api.utils.totp import generate_seed, generate_secret_key

import uuid

def create_user(args):
    if does_user_exist(args["email"]):
        return ""
    
    seed = generate_seed()
    secret = generate_secret_key(seed)
    user = {
        'email': args["email"], 
        'name': args["name"],
        'secret': secret
    }
    
    u_id = uuid.uuid4()
    ref = get_reference(f'users/{u_id}')
    ref.set(user)

    return f'email:{args["email"]}-secret:{secret}'

def does_user_exist(email_to_check):
    users = get_reference('users').get()
    for attr, value in users.items():
        if value['email'] == email_to_check:
            return True
    return False