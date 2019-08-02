#!/usr/bin/env python
from flask import Flask, render_template, Response
import logging
import sys
import os
from multiprocessing import Process, current_process


def trace1(file: object, lineno: object, name: object, pid: object, ppid: object, pr_name: object, dop: object = "") -> object:
    print(f"\t\t\t@#$%| {file} {lineno}\t{name}\tpid={pid} \tparent pid={ppid}\t{pr_name} | {dop}")
    ...


trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name, os.environ)


# emulated camera
from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from camera_file import Camera as CameraDemo

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


@app.route('/demo/')
def demo():
    """Video streaming home page."""
    return render_template('demo.html')


def gen(camera):
    """Video streaming generator function."""
    count = 0
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
    while True:
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        count += 1
        print(f'                           Out a new frame{count} ')
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        frame = camera.get_frame()
        trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/demo_feed')
def demo_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
    return Response(gen(CameraDemo()), mimetype='multipart/x-mixed-replace; boundary=frame')

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
