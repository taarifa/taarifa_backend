from taarifa_backend import db

db_type_to_name = {
    db.DateTimeField: 'DateTime',
    db.StringField: 'String',
    db.FloatField: 'Float'
}


def db_type_to_string(db_type):
    return db_type_to_name.get(db_type, 'Unknown')


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

if __name__ == '__main__':
    print db_type_to_name[db.DateTimeField]
