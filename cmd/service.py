import json

from flask import Flask, request, render_template, jsonify, url_for, g, send_file
import numpy as np
from keras import models as keras_models
import tensorflow as tf

import logging
import os

from werkzeug.utils import secure_filename

from internal import compose
from pkg import clf as clf_pkg
from pkg.io import readers
from pkg.utils import visualizer, inference


app = Flask(os.getenv('SERVICE_NAME'), template_folder=os.getenv('SERVICE_TEMPLATES_FOLDER'))
kwargs = None
graph = None


@app.route('/result', methods=['GET'])
def result():
    """Video streaming home page."""
    logging.info("get_json")
    return render_template('result.html')


@app.route('/get_json', methods=['GET'])
def get_json():
    """Video streaming home page."""
    logging.info("get_json")
    data = json.load(open('static/data.json'))
    return jsonify(data)


@app.route('/get_image', methods=['GET'])
def get_image():
    logging.info("get_image")
    return send_file('static/img/test.png', mimetype='image/gif'), 200


@app.route('/add_files', methods=['POST'])
def add_files():
    logging.info("add_files")
    submitted_file = None
    if len(request.files) > 0:
        submitted_file = request.files['upload']
    print(submitted_file)

    if submitted_file is not None:
        filename = submitted_file.filename
        if allowed_file(filename):
            full_path = os.path.join(kwargs['upload_folder'], 'video.mp4')
            if os.path.exists(full_path):
                os.remove(full_path)
            submitted_file.save(full_path)
            seconds = []
            distributions = []
            for item in clf:
                sec, distr = item
                seconds.append(sec)
                distributions.append(distr)
            visualizer.build_report_image(
                seconds=np.array(seconds),
                distributions=np.array(distributions),
                labels=clf.get_labels(),
                path="static/img/test.png",  # kwargs['image_report_path'],
            )

            g.file = "static/img/test.png"
            g.json = "static/img/test.json"
            data = {
                'seconds': np.array(seconds).tolist(),
                'distributions': np.array(distributions).tolist(),
                'labels': clf.get_labels(),
            }
            with open('static/data.json', 'w') as fd:
                json.dump(data, fd)
            return data, 200
    else:
        return render_template(url_for('index', title='Файл не отправлен')), 422


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    logging.info("index")
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in kwargs['allowed_extension']


def set_config(**kwargs):
    """
    :param kwargs:
    :return:
    """
    log_level = kwargs.get('logging_level', logging.DEBUG)
    log_level = logging.DEBUG
    log_filename = kwargs.get('logging_filename', None)
    log_format = '%(asctime)-15s %(levelname)s [%(name)s] [in %(pathname)-10s:%(funcName)-20s:%(lineno)-5d]: ' \
                 '%(message)s'
    logging.basicConfig(
        format=log_format,
        level=log_level,
        filemode='w',
    )


def init():
    # Этот хак нужен, чтобы граф запускался в том же потоке, что и flask (Спасибо Пете Козыреву и)
    global face_detection, emotion_classifier, graph
    # loading models
    face_detection = inference.load_detection_model(kwargs['face_detection_model_path'])
    emotion_classifier = keras_models.load_model(kwargs['emotion_model_path'], compile=False)
    graph = tf.get_default_graph()


if __name__ == '__main__':
    kwargs = compose.service()
    init()
    log_level = kwargs.get('logging_level', logging.DEBUG)
    log_format = '%(asctime)-15s %(levelname)s [%(name)s] [in %(pathname)-10s:%(funcName)-20s:%(lineno)-5d]: ' \
                 '%(message)s'
    logging.basicConfig(
        format=log_format,
        level=log_level,
        filemode='w',
    )

    reader = readers.VideoFileReader(kwargs['upload_folder']+kwargs['video_name'])
    clf = clf_pkg.EmotionClassifier(
        reader=reader,
        offsets=kwargs['emotion_model']['offset'],
        face_detector=face_detection,
        emotion_detector=emotion_classifier,
        graph=graph,
    )
    app.run(host='0.0.0.0', port=10012, debug=False)
