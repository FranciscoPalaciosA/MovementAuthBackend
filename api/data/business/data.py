import os
import uuid
from pathlib import Path

import cv2
import numpy as np
import io
from api.utils.fire import get_reference
from api.utils.predict import predict_json
from api.utils.totp import generate_secret_key, generate_seed, get_totp_token
from matplotlib.figure import Figure

SHAPE_TO_CHAR = {
    'Circle': 'F',
    'Diamond': 'Y',
    'Triangle': 'N',
    'S_Shape': '2',
    'Infinity': '4',
    'Square': '7'
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
    image_arr = make_plot(data_obj['movement_data'])
    ml_shape = predict(image_arr)

    return ml_shape[0] == data_obj['movement']

def convert_to_sequence(data_obj):
    if 'movement_data' not in data_obj:
        return False
    
    seq = []
    for item in data_obj['movement_data']:
        image_arr = make_plot(item)
        ml_shape = predict(image_arr)
        print(ml_shape)
        seq.append(SHAPE_TO_CHAR[ml_shape[0]])

    print("sequence returned = ", seq)   
    return seq

def make_plot(matrix):
    fig = Figure()
    ax = fig.subplots()
    ax.plot(matrix['x'], matrix['z'])
    ax.axis('off')
    
    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='raw')
    io_buf.seek(0)
    img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                        newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
    io_buf.close()

    return img_arr
    

def predict(image_arr):
    grayed_test = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
    instance = grayed_test.reshape(1,-1)
    return predict_json(instance.tolist(), 'V1')
    
    
