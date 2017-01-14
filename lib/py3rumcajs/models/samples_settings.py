from wtforms_alchemy import ModelForm
from lib.py3rumcajs.app_config.app_config import AppConfig

app_config = AppConfig.instance()
db = app_config.db


class SamplesSettings(db.Model):
    __tablename__ = 'sample_settings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    prefix_x = db.Column(db.String(), nullable=False)
    prefix_y = db.Column(db.String(), nullable=False)
    solution_at_x = db.Column(db.Float(), nullable=False)
    solution_at_y = db.Column(db.Float(), nullable=False)
    mi = db.Column(db.Float(), nullable=False)
    k = db.Column(db.Float(), nullable=False)
    alpha = db.Column(db.Float(), nullable=False, default=25)


class SamplesSettingsForm(ModelForm):
    class Meta:
        model = SamplesSettings
        strip_string_fields = True
