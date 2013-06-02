import datetime
from flask import url_for
from taarifa_backend import db


class BasicReport(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    desc = db.StringField(required=False)
    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)

    description = "Basic location based report"
    keywords = ['basic', 'location', 'report']
    group = 'location based reports'
    service_name = 'basic report'
    service_code = '0001'
    protocol_type = None

    def __unicode__(self):
        return ','.join(map(str, [self.created_at, self.title, self.desc, self.latitude, self.longitude]))

class AdvancedReport(BasicReport):
    complicated_information = db.StringField(max_length=255, required=False)
    advanced_stuff = db.StringField(required=False)
    advanced_date = db.DateTimeField(required=False)

    description = "Extension of the Basic Report"
    keywords = ['advanced', 'cool', 'report', 'location']
    service_name = 'advanced report'
    service_code = '0002'

def get_available_services():
    return [BasicReport, AdvancedReport]
