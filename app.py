#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, shutil

from lib.py3rumcajs.app_config.app_config import AppConfig
AppConfig.initialize(__name__)

from werkzeug import secure_filename
from flask import (render_template,
                   request,
                   redirect,
                   url_for,
                   send_from_directory,
                   flash,
                   )
from lib.py3rumcajs.helpers.file_processing import (validate_file,
                                                    remove_duplicates,
                                                    )
from lib.py3rumcajs.models.datasample import (SampleTypeSettings,
                                              SampleType,
                                              Sample,
                                              )
from lib.py3rumcajs.exceptions.exceptions import SampleValidationException

app_config = AppConfig.instance()
app = app_config.app
db = app_config.db


@app.route('/show/')
def show():
    return render_template('show_settings.html', items=SampleTypeSettings
                           .query.all())


@app.route('/upload', methods=['POST', 'GET', 'DELETE'])
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
            print(type(file))
            validate_file(file)
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_dir, filename))
            remove_duplicates(os.path.join(upload_dir, filename))
            filenames.append(filename)
        except SampleValidationException:
            if file.filename: # TODO FIX
                flash(file.filename + ' is not valid' + file.name)
        except IsADirectoryError:
            pass
        except Exception as exception:
            flash(exception)
    return render_template('uploaded.html', filenames=set(filenames), can_process=True)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run()

