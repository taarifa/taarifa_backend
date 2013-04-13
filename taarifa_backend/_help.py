from taarifa_backend import db

db_type_to_name = {
    db.DateTimeField: 'DateTime',
    db.StringField: 'String',
    db.FloatField: 'Float'
}

def db_type_to_string(db_type):
    return db_type_to_name.get(db_type, 'Unknown')

if __name__ == '__main__':
    print db_type_to_name[db.DateTimeField]
