from wtforms_alchemy import ModelForm
from lib.py3rumcajs.app_config.app_config import AppConfig
from lib.py3rumcajs.models.users import User
import sqlalchemy as sa

app_config = AppConfig.instance()
db = app_config.db

prefix_enum = sa.Enum('pico', 'nano', 'mikro', 'mili', 'uni', 'kilo', 'mega',
                      name='prefix')


class SamplesSettings(db.Model):
    __tablename__ = 'sample_settings'

    id = db.Column(db.Integer, primary_key=True)
    need_process = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(), nullable=False)
    prefix_x = db.Column(prefix_enum, nullable=False)
    prefix_y = db.Column(prefix_enum, nullable=False)
    solution_at_x = db.Column(db.Float(), nullable=False)
    solution_at_y = db.Column(db.Float(), nullable=False)
    mi_k = db.Column(db.Float(), nullable=False)
    alpha = db.Column(db.Float(), nullable=False, default=25)
    r = db.Column(db.Float(), nullable=False)

    # user relation
    user_id = db.Column(db.Integer, db.ForeignKey('flask_user.id'),
                        nullable=False)
    user = db.relationship("User")


class SamplesSettingsForm(ModelForm):
    class Meta:
        model = SamplesSettings
        strip_string_fields = True
        exclude = ['need_process']
