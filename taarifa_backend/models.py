import datetime

from flask_security import RoleMixin, UserMixin
from flask_mongoengine.wtf import model_form

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


class Field(db.EmbeddedDocument):
    """Field in a :class:`Service`."""
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
    """A service schema served by the API."""
    meta = {'strict': False}

    name = db.StringField(required=True)
    fields = db.DictField(required=True)
    description = db.StringField()
    group = db.StringField()
    keywords = db.ListField(db.StringField())
    protocol_type = db.StringField()
    service_name = db.StringField(required=True)
    service_code = db.StringField(required=True, unique=True)


def build_schema(service):
    build_field = lambda d: fieldmap[d.pop('type')](**d)
    return type(str(service.name), (Report,),
                dict(description=service.description,
                     group=service.group,
                     keywords=service.keywords,
                     protocol_type=service.protocol_type,
                     service_name=service.service_name,
                     service_code=service.service_code,
                     meta={'allow_inheritance': True},
                     **dict((k, build_field(v)) for k, v in service.fields.items()))
                )


class Metadata(object):

    """
    Description of a service
    """

    def __init__(self, service_code, service_name, description, group=None):
        self.service_code = service_code
        self.service_name = service_name
        self.description = description
        self.group = group

    def __repr__(self):
        args = [self.service_code, self.service_name, self.description, self.group]
        return 'Metadata(%s)' % ', '.join(map(str, args))


class Report(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)

    latitude = db.FloatField(required=True)
    longitude = db.FloatField(required=True)

    meta = {'allow_inheritance': True, 'strict': False}

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
