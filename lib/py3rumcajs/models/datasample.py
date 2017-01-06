from lib.py3rumcajs.app_config.app_config import AppConfig
from sqlalchemy.dialects.postgresql import JSON

app_config = AppConfig.instance()
db = app_config.db


class Sample(db.Model):
    __tablename__ = 'Sample'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sample = db.Column(JSON)

    sample_type_id = db.Column(db.Integer, db.ForeignKey("SampleType.id"))
    sample_type = db.relationship("SampleType",
                               back_populates="sample")

    def __init__(self, name, sample, sample_type):
        self.name = name
        self.sample = sample
        self.sample_type = sample_type


class SampleType(db.Model):
    __tablename__ = 'SampleType'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sample = db.relationship("Sample", back_populates="sample_type")

    settings_id = db.Column(db.Integer, db.ForeignKey("SampleTypeSettings.id"))
    settings = db.relationship("SampleTypeSettings",
                               back_populates="sample_type")



    def __init__(self, name):
        self.name = name


class SampleTypeSettings(db.Model):
    __tablename__ = 'SampleTypeSettings'

    id = db.Column(db.Integer, primary_key=True)
    # TODO user relation in future

    sample_type = db.relationship("SampleType", back_populates="settings")


