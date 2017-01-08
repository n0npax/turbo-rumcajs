#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import json

from app_celery import make_celery
from werkzeug import secure_filename
from flask_redis import FlaskRedis

from lib.py3rumcajs.algorithms.common import calibrate, compute_deltas

from lib.py3rumcajs.exceptions.exceptions import SampleValidationException
from lib.py3rumcajs.app_config.app_config import AppConfig
# cross dependency fo AppConfig instance (singleton)
AppConfig.initialize(__name__)

from lib.py3rumcajs.helpers.file_processing import (validate_file,
                                                    rescale_data,
                                                    )
from lib.py3rumcajs.models.datasample import (SampleTypeSettings,
                                              SampleType,
                                              Sample,
                                              )
from flask import (render_template,
                   request,
                   redirect,
                   url_for,
                   send_from_directory,
                   flash,
                   session,
                   jsonify,
                   )

app_config = AppConfig.instance()
app = app_config.app
app.config.update(CELERY_BROKER_URL='redis://localhost:6379',
                  CELERY_RESULT_BACKEND='redis://localhost:6379')
celery = make_celery(app)
redis_store = FlaskRedis(app)
db = app_config.db


from tasks import process_files, process_file

@app.route('/show/')
def show():
    return render_template('show_settings.html', items=SampleTypeSettings
                           .query.all())


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



@app.route('/upload/', methods=['POST', 'GET', 'DELETE'])
def upload():
    upload_dir = app.config['UPLOAD_FOLDER']
    uploaded_files = request.files.getlist("file[]")
    uploaded_calibration = request.files.getlist("calibration_file")
    if uploaded_calibration:
        uploaded_calibration[0].filename = 'Calibration.txt'
        uploaded_files.append(uploaded_calibration[0])
    filenames = os.listdir(upload_dir)
    if request.method == 'DELETE':
        shutil.rmtree(upload_dir)
        os.mkdir(upload_dir)
    for file in uploaded_files:
        try:
            validate_file(file)
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_dir, filename))
            filenames.append(filename)
        except SampleValidationException:
            if file.filename:  # TODO FIX
                flash(file.filename + ' is not valid' + file.name)
        except IsADirectoryError:
            pass
        except Exception as exception:
            flash(exception)
    return render_template('uploaded.html', filenames=set(filenames),
                           can_process=True)
    # TODO

@app.route('/process/', methods=['POST','GET'])
def process():
    if request.method == 'POST':
        upload_dir = app.config['UPLOAD_FOLDER']
        filenames = os.listdir(upload_dir)
        # mock celery for debug
        for filename in filenames:
            data = process_file(upload_dir, filename)
            redis_store.set(filename, json.dumps(data))
            redis_store.set('filenames', json.dumps(filenames))
        # mock end

        task = process_files.delay(upload_dir, filenames)
        return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}
    if request.method == 'GET':
        return render_template('process.html')


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = process_files.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@app.route('/graph/', defaults={'filename': None})
@app.route('/graph/<filename>')
def graph(filename):
        filenames = json.loads(redis_store.get('filenames').decode('utf-8'))
        data, calibration = {}, {}
        if filename:
            calibration = json.loads(redis_store.get('Calibration.txt')
                                     .decode('utf-8'))
            data = json.loads(redis_store.get(filename).decode('utf-8'))
            data = calibrate(data)
            compute_deltas(data, calibration)
        return render_template('graph.html', data=data, filenames=filenames,
                                calibration=calibration)


if __name__ == '__main__':
    app.run()

