import datetime

from flask.ext.security import RoleMixin, UserMixin
from flask.ext.mongoengine.wtf import model_form

from taarifa_backend import db
from taarifa_backend.utils import get_mongoengine_class, fieldmap


class ReportField(db.EmbeddedDocument):
    """Description of a field in a report"""
    # TODO: must be a python field name, check or always correct this
    name = db.StringField(required=True)
    fieldtype = db.StringField(required=True, choices=fieldmap.keys())
    # mongoengine properties of a Field
    db_field = db.StringField(default=None)
    required = db.BooleanField(default=False)
    default = db.DynamicField(default=None)
    unique = db.BooleanField(default=False)
    unique_with = db.DynamicField(default=None)
    primary_key = db.BooleanField(default=False)
    choices = db.DynamicField(default=None)
    help_text = db.StringField(default=None)
    verbose_name = db.StringField(default=None)


class Service(db.Document):
    """A service schema served by the API.

    Describes the fields and validations of a certain type of report
    """
    # Must be a valid python class name
    # TODO: Have to check or correct this
    classname = db.StringField(required=True)
    service_name = db.StringField(required=True)
    service_code = db.StringField(required=True, unique=True)
    fields = db.ListField(field=db.EmbeddedDocumentField(ReportField))
    description = db.StringField()
    group = db.StringField()
    keywords = db.ListField(db.StringField())
    protocol_type = db.StringField()


def create_db_field(field):
    """creates a mongoengine field from the description contained in a :class:`ReportField`"""
    _class = get_mongoengine_class(field.fieldtype)
    return _class(db_field=field.db_field, required=field.required, default=field.default,
                  unique=field.unique, unique_with=field.unique_with,
                  primary_key=field.primary_key, choices=field.choices,
                  help_text=field.help_text, verbose_name=field.verbose_name)


def build_schema(service):
    """dynamically creates the :class:`Report` for the given :class:`Service`"""
    fields = dict([(f.name, create_db_field(f)) for f in service.fields])
    return type(str(service.classname), (Report, ), fields)


class Report(db.Document):
    """base class used for all created Reports"""
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)

    meta = {'allow_inheritance': True}

ReportForm = model_form(Report, exclude=['created_at'])


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


def get_available_services():
    return [build_schema(o) for o in Service.objects]


def get_service_class(service_code):
    try:
        return build_schema(Service.objects.get(service_code=service_code))
    except Service.DoesNotExist:
        return Report


def get_form(service_code):
    return model_form(get_service_class(service_code), exclude=['created_at'])


def clear_database():
    for cls in [Report, Role, User]:
        cls.drop_collection()
