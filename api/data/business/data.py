from api.utils.fire import get_reference
from api.utils.totp import generate_seed, generate_secret_key, get_totp_token

import uuid

SHAPE_TO_CHAR = {
    'Circle': 'A',
    'Diamond': 'D',
    'Triangle': 'M',
    'S_Shape': '1',
    'Infinity': '3',
    'Square': '9'
}

def upload_movement(data_obj):
    print(data_obj)
    if 'movement' not in data_obj or 'movement_data' not in data_obj:
        return False
    ref = get_reference(f'data/{data_obj["movement"]}')
    data = data_obj["movement_data"]
    pushed_ref = ref.push(data)
    return True

def check_movement(data_obj):
    if 'movement' not in data_obj or 'movement_data' not in data_obj:
        return False
    
    # Run ML 
    ml_shape = 'Circle'
    return ml_shape == data_obj['movement']

def convert_to_sequence(data_obj):
    if 'movement_data' not in data_obj:
        return False
    
    seq = []
    for item in data_obj['movement_data']:
        # Run ML for each
        seq.append(SHAPE_TO_CHAR['Circle'])
    return seq