from api.utils.fire import get_reference
from api.utils.totp import generate_seed, generate_secret_key, get_totp_token

import uuid

def upload_movement(data_obj):
    print(data_obj)
    if 'movement' not in data_obj or 'movement_data' not in data_obj:
        return False
    ref = get_reference(f'data/{data_obj["movement"]}')
    data = data_obj["movement_data"]
    pushed_ref = ref.push(data)
    return True
