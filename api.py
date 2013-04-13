from flask import Flask, request
from taarifa_backend import app
from models import Report
import json

logger = app.logger

@app.route("/reports", methods=['POST'])
def receive_report():
    """
    post report to the backend
    """
    logger.debug('Report post received')
    logger.debug('JSON: ' + request.json.__repr__())

    save_report(request.json)
    
    # Check database
    reports = Report.objects.all()
    logger.debug('Reports in the database \n' + ', '.join(map(lambda x: x.__repr__(), reports)))

    return "Report post received"

def verify_report(report):
    expected_fields = ['title', 'longitude', 'latitude']
    report_ok = len(expected_fields) == len(report.keys());
    for f in report.keys():
        if f not in expected_fields:
            logger.debug('Field %s was unexpected. Possible fields are: %s. Report has not been saved' % (f, ', '.join(expected_fields)))
            report_ok = False
    return report_ok

def save_report(report):
    report_ok = verify_report(report)
    if not report_ok:
        return

    for k,v in report.iteritems():
        if k in ['longitude', 'latitude']:
            report[k] = float(v)
    r = Report(**report)
    r.save()
