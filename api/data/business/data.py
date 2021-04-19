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

def get_avg(arr):
    s = 0
    for i in arr:
        s = s + i
    return 255 -  s / len(arr)

def compress_matrix(matrix):
    h, w = matrix.shape
    new_h = int(h / 4)
    new_w = int(w / 4)
    jump = 4

    compressed_matrix = np.zeros((new_h, new_w))
    for i in range(new_h):
        for j in range(new_w):
            nums_to_avg = []
            for k in range(4):
                for l in range(4):
                    nums_to_avg.append(matrix[i * jump + k][j * jump + l])
            compressed_matrix[i][j] = get_avg(nums_to_avg)
    return compressed_matrix

def upload_movement(data_obj):
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
    compressed_matrix = compress_matrix(image_arr)
    print("compressed matrix = ", compressed_matrix)
    ml_shape = predict(compressed_matrix.reshape(1,-1))

    return ml_shape[0] == data_obj['movement']

def convert_to_sequence(data_obj):
    if 'movement_data' not in data_obj:
        return False
    
    instances = []
    for item in data_obj['movement_data']:
        image_arr = make_plot(item)
        compressed_matrix = compress_matrix(image_arr)
        compressed_matrix = compressed_matrix.reshape(1, -1)
        instances.append(compressed_matrix[0].tolist())
    predictions = predict_multiple(instances)
    seq = []
    for pred in predictions:
        seq.append(SHAPE_TO_CHAR[pred])
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
    
    grayed_img = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    return grayed_img
    

def predict_multiple(instances):
    return predict_json(instances, 'V2')

def predict(instance):
    return predict_json(instance.tolist(), 'V2')
    
    
