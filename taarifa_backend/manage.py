# Set the path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server

from taarifa_backend import app
from taarifa_backend.models import clear_database, Role, User, Service, ReportField

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)


# Setup roles and initial admin user
@manager.option("-e", "--email", dest="email", required=True,
                help="Email address (required)")
@manager.option("-c", "--clean", dest="clean", action="store_true",
                default=False, help="Clear the user and role database")
def setup(email, clean):
    """Create a new admin user with given email address."""
    if clean:
        clear_database()

    role, _ = Role.objects.get_or_create(name="admin",
                                         defaults={'description': 'Taarifa Admin'})
    _, created = User.objects.get_or_create(email=email, defaults={'roles': [role]})
    if not created:
        print "User with email address %s did already exist and was not created" % email


@manager.command
def create_services():
    """Create default service types BasicReport and Waterpoint."""
    Service(classname="Generic",
            fields=[ReportField(name="title", fieldtype="StringField",
                                max_length=255, required=True),
                    ReportField(name="desc", fieldtype="StringField",
                                required=True)],
            description="Generic location based report",
            keywords=["location", "report"],
            group="location",
            service_name="basic report",
            service_code="0001").save()
    Service(classname="Waterpoint",
            fields=[ReportField(name="waterpoint_id", fieldtype="StringField",
                                required=True),
                    ReportField(name="functional", fieldtype="BooleanField",
                                required=True)],
            description="Location, description and functionality of a waterpoint",
            keywords=["location", "report", "water"],
            group="water",
            service_name="waterpoint",
            service_code="wp001").save()

if __name__ == "__main__":
    manager.run()
