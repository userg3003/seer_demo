#!/usr/bin/env python
from flask import (Flask,  request, redirect, url_for, render_template,
                    session, g, jsonify, current_app)

from werkzeug.utils import secure_filename
import logging
import sys
import os
import json
from multiprocessing import Process, current_process

from utils import trace1

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['mp4', 'avi', 'py'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """SEER home page."""
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    """SEER result page."""
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
    req = request.form.to_dict()
    return render_template('result.html', file_pict=req["file_pict_name"], file_json=req["file_json_name"])


@app.route('/add_files', methods=['POST'])
def add_files():
    trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
    logging.getLogger().info("add_request")

    logging.getLogger().info(request.form.to_dict())
    count_error = -1
    error = True
    while error and count_error <= 5:
        try:
            error = False
        except Exception as err:
            count_error += 1
            error = True
            logging.getLogger().debug(f"count_error={count_error}  Error:{err} ")
    logging.getLogger().debug("")

    logging.getLogger().debug(request.form.to_dict())
    if len(request.files) > 0:
        submitted_file = request.files['upload']
    else:
        submitted_file = None
    if submitted_file is not None:
        filename = submitted_file.filename

    if submitted_file is not None:
        if allowed_file(filename):
            filename = secure_filename(filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(full_path):
                os.remove(full_path)
            submitted_file.save(full_path)
            file_name_pict = "seer_result.png"
            file_name_json = "seer_result.json"
            path_for_pict = f"./static/img/{file_name_pict}"
            path_for_json = f"./static/{file_name_json}"
            seconds = []
            distributions = []
            # for item in clf:
            #     sec, distr = item
            #     seconds.append(sec)
            #     distributions.append(distr)
            # visualizer.build_report_image(
            #     seconds=np.array(seconds),
            #     distributions=np.array(distributions),
            #     labels=clf.get_labels(),
            #     path=kwargs['image_report_path'],
            # )

            trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
            data = {
                'info': {
                    'file_pict_name': file_name_pict,
                    'file_json_name': file_name_json,
                    "status": "success"
                }
            }
            response = jsonify(data)
            response.status_code = 201
            trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
            if submitted_file is not None:
                trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
                return response
            trace1(__file__, sys._getframe().f_lineno, __name__, os.getpid(), os.getppid(), current_process().name)
            return redirect(url_for('index', _method="GET"), 302)
    else:
        return render_template(url_for('index', title='Файл не отправлен'))




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



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
    app.run(host='127.0.0.1', debug=True, threaded=True)
