from flask_user import UserMixin
from lib.py3rumcajs.app_config.app_config import AppConfig

app_config = AppConfig.instance()
db = app_config.db


# Define User model. Make sure to add flask_user UserMixin !!!
class User(UserMixin, db.Model):
    __tablename__ = 'flask_user'

    id = db.Column(db.Integer, primary_key=True)

    # User Authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')

    # User Email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    # University
    university = db.Column(db.String(50), nullable=False, default='')

    def is_active(self):
        return self.is_enabled
