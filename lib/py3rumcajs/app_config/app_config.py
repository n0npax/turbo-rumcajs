import os
from singleton.singleton import Singleton
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

@Singleton
class AppConfig(object):

    def __init__(self, name=None):
        if name:
            self.app = Flask(name)
            self.app.config['UPLOAD_FOLDER'] = 'uploads/'
            self.app.config.from_object(os.environ['APP_SETTINGS'])
            self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
            self.db = SQLAlchemy(self.app)


