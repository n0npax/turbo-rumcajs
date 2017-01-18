#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import json

from app_celery import make_celery
from werkzeug import secure_filename
from flask_redis import FlaskRedis

from lib.py3rumcajs.algorithms.common import (calibrate,
                                             compute_deltas,
                                             )
from lib.py3rumcajs.algorithms.elasticity import compute_elasticity

from lib.py3rumcajs.exceptions.exceptions import SampleValidationException
from lib.py3rumcajs.app_config.app_config import AppConfig
# cross dependency fo AppConfig instance (singleton)
AppConfig.initialize(__name__)

from lib.py3rumcajs.helpers.file_processing import (validate_file,
                                                    rescale_data,
                                                    )
from lib.py3rumcajs.models.samples_settings import (SamplesSettings,
                                                    SamplesSettingsForm,
                                                    )
from lib.py3rumcajs.models.users import User
from flask_mail import Mail

from flask import (render_template,
                   request,
                   redirect,
                   url_for,
                   send_from_directory,
                   flash,
                   session,
                   jsonify,
                   )

from flask_user import (login_required,
                        LoginManager,
                        UserManager,
                        SQLAlchemyAdapter,
                        )

from flask_wtf import Form
from wtforms.ext.appengine.db import model_form

app_config = AppConfig.instance()
app = app_config.app
app.config.update(CELERY_BROKER_URL='redis://localhost:6379',
                  CELERY_RESULT_BACKEND='redis://localhost:6379')
celery = make_celery(app)
redis_store = FlaskRedis(app)
db = app_config.db

# Flask-User
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)
mail = Mail(app)

login_manager = LoginManager()

from tasks import process_files, process_file

from wtforms.ext.sqlalchemy.orm import model_form


def get_upload_dir():
    return app.config['UPLOAD_FOLDER'] + get_user_name() + '/'


@login_required
def get_user_name():
    if 'user_id' in session:
        id = session['user_id']
        return User.query.filter_by(id=id).first().username
    raise Exception('not authorized user')


@login_required
def get_user_id():
    if 'user_id' in session:
        return session['user_id']
    raise Exception('not authorized user')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    obj = SamplesSettings.query.first()
    if not obj:
        obj = SamplesSettings()
    if request.method == 'POST':
        form = SamplesSettingsForm(request.form)
        if form.validate():
            form.populate_obj(obj)
            obj.user_id = get_user_id()  # force user bind
            db.session.merge(obj)
            flash('settings updated')
            db.session.commit()
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text, error))
    form = SamplesSettingsForm(obj=obj)
    return render_template('settings.html', form=form)


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(get_upload_dir(),
                               filename)


@app.route('/upload/', methods=['POST', 'GET', 'DELETE'])
@login_required
def upload():
    upload_dir = get_upload_dir()
    uploaded_files = request.files.getlist("file[]")
    uploaded_calibration = request.files.getlist("calibration_file")
    if uploaded_calibration:
        uploaded_calibration[0].filename = 'Calibration.txt'
        uploaded_files.append(uploaded_calibration[0])
    if not os.path.isdir(upload_dir):
        os.mkdir(upload_dir)
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
    # TODO can_process is HARDCODED


@app.route('/process/', methods=['POST', 'GET'])
@login_required
def process():
    if request.method == 'POST':
        upload_dir = get_upload_dir()
        filenames = os.listdir(upload_dir)
        settings = SamplesSettings.query \
            .filter_by(user_id=get_user_id()).first()

        # mock celery for debug
        for filename in filenames:
            data = process_file(upload_dir, filename, settings)
            redis_store.set(filename, json.dumps(data))
            redis_store.set('filenames', json.dumps(filenames))
        # mock end

        task = process_files.delay(upload_dir, filenames, settings)
        return jsonify({}), 202, {'Location': url_for('taskstatus',
                                  task_id=task.id)}
    if request.method == 'GET':
        return render_template('process.html')


@app.route('/status/<task_id>')
@login_required
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
@login_required
def graph(filename):
        filenames = json.loads(redis_store.get('filenames').decode('utf-8'))
        data, calibration = {}, {}
        if filename:
            calibration = json.loads(redis_store.get('Calibration.txt')
                                     .decode('utf-8'))
            data = json.loads(redis_store.get(filename).decode('utf-8'))
            data = calibrate(data)
            compute_deltas(data, calibration)
            settings = SamplesSettings.query \
                .filter_by(user_id=get_user_id()).first()
            compute_elasticity(data, settings)
        return render_template('graph.html', data=data, filenames=filenames,
                               calibration=calibration)


if __name__ == '__main__':
    app.run()
