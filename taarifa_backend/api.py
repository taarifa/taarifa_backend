from flask import Flask, request, jsonify, render_template, make_response
from taarifa_backend import app
from models import BasicReport
from utils import crossdomain, jsonp
import models
import json
import _help
import pprint

logger = app.logger

def get_services():
    response = {}

    services = models.get_available_services()
    for service_description in services:
        logger.debug(service_description)
        service_name = str(service_description.__name__)
        logger.debug(service_name)

        fields = service_description._fields
        logger.debug(fields)

        service = {}
        field_dict = {}
        for name, f in fields.iteritems():
            if name in ['id', 'created_at']:
                continue
            field = {}
            field['required'] = str(f.required)
            field['type'] = _help.db_type_to_string(f.__class__)
            field_dict[name] = field
        service['fields'] = field_dict
        for key in ['protocol_type', 'keywords', 'service_name', 'service_code', 'group', 'description']:
            service[key] = getattr(service_description, key)
        logger.debug(service)
        response[service_name] = service
    return response

@app.route("/")
def landing():
    return render_template('landing.html', services=pprint.pformat(get_services()))

@app.route("/reports", methods=['POST'])
@crossdomain(origin='*', headers="Origin, X-Requested-With, Content-Type, Accept")
def receive_report():
    """
    post report to the backend
    """
    logger.debug('Report post received')
    logger.debug('JSON: ' + request.json.__repr__())

    _save_report(request.json)
    
    # Check database
    reports = BasicReport.objects.all()
    logger.debug('Reports in the database \n' + ', '.join(map(lambda x: x.__repr__(), reports)))

    return "Report post received\n"

@app.route("/reports", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_all_reports():
    all_reports = BasicReport.objects.all()
    return make_response(json.dumps(map(_help.mongo_to_dict, all_reports)))

@app.route("/reports/<string:id>", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_report(id = False):
    report = BasicReport.objects.with_id(id)
    return jsonify(_help.mongo_to_dict(report))


@app.route("/services", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_list_of_all_services():
    # TODO: factor out the transformation from a service to json
    return jsonify(**get_services())

def _save_report(report):
    report_ok = _verify_report(report)
    if not report_ok:
        return

    for k,v in report.iteritems():
        if k in ['longitude', 'latitude']:
            report[k] = float(v)
    r = BasicReport(**report)
    r.save()

def _verify_report(report):
    expected_fields = ['title', 'longitude', 'latitude']
    report_ok = len(expected_fields) == len(report.keys());
    for f in report.keys():
        if f not in expected_fields:
            logger.debug('Field %s was unexpected. Possible fields are: %s. Report has not been saved' % (f, ', '.join(expected_fields)))
            report_ok = False
    return report_ok
