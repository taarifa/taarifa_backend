import logging
import json

from flask import Blueprint, request, jsonify, render_template, make_response, redirect, flash
from flask.ext.security import http_auth_required
from flask.ext.mongoengine.wtf import model_form
import mongoengine

import models
from taarifa_backend import user_datastore
from utils import crossdomain, jsonp, db_type_to_string, mongo_to_dict

logger = logging.getLogger(__name__)

api = Blueprint("api", __name__, template_folder='templates')


def get_services():
    response = {}

    services = models.get_available_services()
    for service in services:
        res = dict((key, getattr(service, key, None))
                   for key in ['protocol_type', 'keywords', 'service_name',
                               'service_code', 'group', 'description'])
        fields = {}
        for name, f in service._fields.iteritems():
            if name in ['id', 'created_at', '_cls']:
                continue
            fields[name] = {
                'required': f.required,
                'type': db_type_to_string(f.__class__)
            }
        res['fields'] = fields
        response[service.__name__] = res
    return response


@api.route("/")
def landing():
    return render_template('landing.html', services=get_services())


@api.route("/map")
def carto():
    return render_template('map.html')


@api.route("/reports", methods=['POST'])
@crossdomain(origin='*', headers="Origin, X-Requested-With, Content-Type, Accept")
def receive_report():
    """
    post report to the backend
    """
    logger.debug('Report post received')
    logger.debug('JSON: %r' % request.json)

    # TODO: Deal with errors regarding a non existing service code
    service_code = request.json['service_code']
    service_class = models.get_service_class(service_code)

    # TODO: Handle errors if the report field is not available
    data = request.json['data']
    data.update(dict(service_code=service_code))
    db_obj = service_class(**data)

    try:
        doc = db_obj.save()
    except mongoengine.ValidationError, e:
        logger.debug(e)
        # TODO: Send specification of the service used and a better error
        # description
        return jsonify({'Error': 'Validation Error'})

    return jsonify(mongo_to_dict(doc))


@api.route("/reports/add", methods=['GET', 'POST'])
def add_report():
    service_code = request.args.get('service_code', None)
    service = models.get_service_class(service_code)
    form = model_form(service, exclude=['created_at'])(request.form)
    # FIXME: use form.validate_on_submit() once it's working
    if form.is_submitted():
        doc = service(**form.data)
        logger.debug(form.data)
        doc.save()
        flash("Report successfully submitted!")
        return redirect('/reports')
    return render_template('add_report.html', form=form, report=service.__name__)


@api.route("/reports", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_all_reports():
    service_code = request.args.get('service_code', None)

    service_class = models.get_service_class(service_code)

    all_reports = service_class.objects.all()

    return make_response(json.dumps(map(mongo_to_dict, all_reports)))


@api.route("/reports/<string:id>", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_report(id=False):
    # TODO: This is still using BasicReport, should be moved to service based
    # world
    report = models.Report.objects.get(id=id)
    return jsonify(mongo_to_dict(report))


@api.route("/services", methods=['POST'])
@crossdomain(origin='*', headers="Origin, X-Requested-With, Content-Type, Accept")
def create_service():
    logger.debug('Service post received')
    logger.debug('JSON: %r' % request.json)

    db_obj = models.Service(**request.json)

    try:
        doc = db_obj.save()
    except mongoengine.ValidationError as e:
        logger.debug(e)
        # TODO: Send specification of the service used and a better error
        # description
        return jsonify({'Error': 'Validation Error'})

    return jsonify(mongo_to_dict(doc))


@api.route("/services", methods=['GET'])
@crossdomain(origin='*')
@jsonp
def get_list_of_all_services():
    # TODO: factor out the transformation from a service to json
    return jsonify(**get_services())


@api.route("/admin", methods=["POST"])
@http_auth_required
@crossdomain(origin='*', headers="Origin, X-Requested-With, Content-Type, Accept")
@jsonp
def create_admin():
    """
    create an admin in the backend
    """
    logger.debug('New admin received')
    logger.debug('JSON: %r' % request.json)

    # TODO: Deal with errors regarding a non existing service code
    required = ["email", "password"]
    missing = list(set(required) - set(request.json.keys()))
    if missing:
        response = jsonify({"Error": "Validation Error",
                            "Missing": missing})
        response.status_code = 422
        return response

    try:
        user = user_datastore.create_user(email=request.json["email"],
                                          password=request.json["password"])
    except mongoengine.ValidationError:
        return jsonify({'Error': 'Validation Error'})

    return jsonify(mongo_to_dict(user))
