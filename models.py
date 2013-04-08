import datetime
from flask import url_for
from taarifa_backend import db


class Report(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)

    def __unicode__(self):
        return ','.join(map(str, [self.created_at, self.title, self.latitude, self.longitude]))


