#!/usr/bin/env python
from flask import (Flask, render_template, Response, request, flash, request, redirect, url_for, render_template,
                    session, g)

from werkzeug.utils import secure_filename
import logging
import sys
import os
from multiprocessing import Process, current_process

from utils import trace1
from filesjpeg import FilesJpeg
from video_file import VideoFile

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['mp4', 'avi'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/src')
@app.route('/index_src')
def index_src():
    """Video streaming home page."""
    return render_template('index_src.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(full_path):
                os.remove(full_path)
            file.save(full_path)
            return redirect(url_for('index', filename=filename))
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/demo_jpeg')
def demo_jpeg():
    """Video streaming home page."""
    return render_template('demo_jpeg.html')


def gen(camera):
    """Video streaming generator function."""
    count = 0
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
    while True:
        count += 1
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name,
               f'                           Out a new frame{count} ')
        frame = camera.get_frame()
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/jpeg_files')
def jpeg_files():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(FilesJpeg()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/demo_file')
def demo_file():
    """Video streaming home page."""
    return render_template('demo_file.html')


@app.route('/video_file')
def video_file():
    """Video streaming route. Put this in the src attribute of an img tag."""
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
    return Response(gen(VideoFile()), mimetype='multipart/x-mixed-replace; boundary=frame')


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


if __name__ == '__main__':
    logging.debug("")
    set_config()
    logging.debug("")
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name, os.environ)
    app.run(host='0.0.0.0', debug=True, threaded=True)
