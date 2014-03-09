from datetime import timedelta
from functools import update_wrapper, wraps

from flask import make_response, request, current_app

from taarifa_backend import db

fieldmap = {
    'BinaryField': db.BinaryField,
    'BooleanField': db.BooleanField,
    'ComplexDateTimeField': db.ComplexDateTimeField,
    'DateTimeField': db.DateTimeField,
    'DecimalField': db.DecimalField,
    'DictField': db.DictField,
    'DynamicField': db.DynamicField,
    'EmailField': db.EmailField,
    'EmbeddedDocumentField': db.EmbeddedDocumentField,
    'FileField': db.FileField,
    'FloatField': db.FloatField,
    'GenericEmbeddedDocumentField': db.GenericEmbeddedDocumentField,
    'GenericReferenceField': db.GenericReferenceField,
    'GeoPointField': db.GeoPointField,
    'ImageField': db.ImageField,
    'IntField': db.IntField,
    'ListField': db.ListField,
    'MapField': db.MapField,
    'ObjectIdField': db.ObjectIdField,
    'ReferenceField': db.ReferenceField,
    'SequenceField': db.SequenceField,
    'SortedListField': db.SortedListField,
    'StringField': db.StringField,
    'URLField': db.URLField,
    'UUIDField': db.UUIDField,
}


def get_mongoengine_class(fieldtype):
    """gets the associated class reference for the string"""
    return fieldmap[fieldtype]


def mongoengine_class_to_string(_class):
    for k, v in fieldmap.iteritems():
        if v == _class:
            return k
    return 'Unknown'


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function
