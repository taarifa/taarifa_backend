from datetime import timedelta
from functools import update_wrapper, wraps

from flask import make_response, request, current_app

from taarifa_backend import db

db_type_to_name = {
    db.DateTimeField: 'DateTime',
    db.StringField: 'String',
    db.FloatField: 'Float'
}


def db_type_to_string(db_type):
    return db_type_to_name.get(db_type, 'Unknown')


# After http://stackoverflow.com/a/14025561/396967
def mongo_to_dict(obj):
    return_data = []

    if isinstance(obj, db.Document):
        return_data.append(("id", str(obj.id)))

    for field_name in obj._fields:

        if field_name in ("id",):
            continue

        data = obj._data[field_name]

        if data:
            if isinstance(obj._fields[field_name], db.DateTimeField):
                return_data.append((field_name, str(data.isoformat())))
            elif isinstance(obj._fields[field_name], db.StringField):
                return_data.append((field_name, str(data)))
            elif isinstance(obj._fields[field_name], db.FloatField):
                return_data.append((field_name, float(data)))
            elif isinstance(obj._fields[field_name], db.IntField):
                return_data.append((field_name, int(data)))
            elif isinstance(obj._fields[field_name], db.ListField):
                return_data.append((field_name, data))
            elif isinstance(obj._fields[field_name], db.EmbeddedDocumentField):
                return_data.append((field_name, mongo_to_dict(data)))

    return dict(return_data)


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
