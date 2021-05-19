import io
import sys
import logging
from datetime import datetime
from pathlib import Path
import tensorflow as tf
from tensorflow import keras

import cv2
import numpy as np
from api.utils.fire import get_reference
from api.utils.predict import predict_json
from api.utils.totp import generate_secret_key, generate_seed, get_totp_token
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

np.set_printoptions(threshold=sys.maxsize)

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
    return 255 - s / len(arr)

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
            compressed_matrix[i][j] = int(get_avg(nums_to_avg))
    return compressed_matrix

def upload_movement_on_user(data_obj, uid, success):
    if 'movement' not in data_obj or 'movement_data' not in data_obj:
        return False
    ref = get_reference(f'/users_data/{uid}/{data_obj["movement"]}')
    data = data_obj["movement_data"]
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    pushed_ref = ref.push({'data': data, 'timestamp': timestamp, 'success': success})
    return True

def upload_movement(data_obj):
    ref = get_reference(f'get_password_data/')
    data = data_obj
    pushed_ref = ref.push(data)
    return True

def upload_attempt(shape, success):
    ref = get_reference(f'attempts_by_shape/{shape}')
    pushed_ref = ref.push(success)

def create_graph(matrix):
    fig = Figure()
    ax = fig.subplots()
    ax.plot(matrix['x'], matrix['z'])
    ax.axis('off')

    # Write img matrix in memory
    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='raw')
    io_buf.seek(0)
    img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                        newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
    io_buf.close()

    # Change to gray 
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    compressed_matrix = compress_matrix(gray)

    path = f'./compress/shape/'
    Path(path).mkdir(parents=True, exist_ok=True)
    
    # Save image
    cv2.imwrite(path + f'/rwar.png', compressed_matrix)

def check_movement(data_obj):
    if 'movement' not in data_obj or 'movement_data' not in data_obj:
        return False
    image_arr = make_plot(data_obj['movement_data'])
    compressed_matrix = compress_matrix(image_arr).astype(int).reshape(1,-1)
    ml_shape = predict(compressed_matrix)    
    is_movement_correct = ml_shape[0] == data_obj['movement']
    
    upload_movement_on_user(data_obj, data_obj['userId'], is_movement_correct)
    upload_attempt(data_obj['movement'], is_movement_correct)

    return is_movement_correct

def convert_to_sequence(data_obj):
    if 'movement_data' not in data_obj:
        return False
    
    instances = []

    start_time = datetime.now()
    for item in data_obj['movement_data']:
        upload_movement(item)
        image_arr = make_plot(item)
        compressed_matrix = compress_matrix(image_arr)
        compressed_matrix = compressed_matrix.reshape(1, -1)
        instances.append(compressed_matrix[0].tolist())
    predictions = predict_multiple(instances)
    seq = []
    for pred in predictions:
        seq.append(SHAPE_TO_CHAR[pred])
    end_time = datetime.now()
    time_sequence(end_time - start_time)

    logging.info("sequence returned = ", seq)
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
    print("make_plot - img arr =", img_arr.shape)
    grayed_img = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    print("make_plot - greyed image =", grayed_img.shape)
    return grayed_img
    
def predict_multiple(instances):
    return predict_json(instances, 'V2')

def predict(instance):
    return predict_json(instance.tolist(), 'V2')
    
def time_sequence(ms):
    try:
        ref = get_reference('sequence_timing')
        ref.push({'ms': ms.total_seconds() * 1000})
        return True
    except Exception as e:
        print("Error ocurred on saving time = ", e)
        return False


img_height = 160
img_width = 140
movements = [
        'Circle',
        'Diamond',
        'Infinity',
        'S_Shape',
        'Square',
        'Triangle',
        ]
def improved_check_movement(data_obj):
    if 'movement_data' not in data_obj:
        return False
    
    model = tf.keras.models.load_model('./CNNModel')

    plot_data(data_obj['movement_data'])
    img = tf.keras.preprocessing.image.load_img(
            './improved_shapes/shape_movement.png',
            target_size=(img_height, img_width)
            )
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    prediction = model.predict(img_array)
    score = tf.nn.softmax(prediction[0])
    return movements[np.argmax(score)]

def plot_data(matrix):
    fig = Figure()
    ax = fig.subplots()
    ax.plot(matrix['x'], matrix['z'])
    ax.axis('off')

    # Write img matrix in memory
    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='raw')
    io_buf.seek(0)
    img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                        newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
    io_buf.close()

    # Change to gray 
    gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    compressed_matrix = compress_matrix(gray)

    path = f'./improved_shapes'
    Path(path).mkdir(parents=True, exist_ok=True)
    
    # Save image
    cv2.imwrite(path + f'/shape_movement.png', compressed_matrix)

def improved_get_sequence(data_obj):
    if 'movement_data' not in data_obj:
        return False
    seq = []
    for item in data_obj['movement_data']:
        shape_predicted = improved_check_movement({'movement_data': item})
        print("shape_predicted = ", shape_predicted)
        seq.append(SHAPE_TO_CHAR[shape_predicted])
        
    logging.info("sequence returned = ", seq)
    return seq