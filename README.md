taarifa_backend
===============

Prototype of a Taarifa backend

Installation
---------

Install MongoDB: http://docs.mongodb.org/manual/installation/

Run mongo

```
mongod
```

Install python dependencies using pip: http://www.pip-installer.org/en/latest/requirements.html

```
pip install -r requirements.txt
```

Start the server
```
python manage.py runserver
```

Run the curl_send_report script from the console to try sending a report via JSON


API work notes
-----------------

The API will support the following requests:

Services:

Defines a report template, i.e. the set of fields which are part of the report, their type and their contraints.
This is comparable to a custom form.


POST services
Creates a new service
GET services
Gets list of all services

GET services/{service_id}
UPDATE services/{service_id}
DELETE services/{service_id}

Reports:

The collection of information about which a report is made. Must use one previously defined service.

POST reports
Creates a new report.

GET reports
list of all reports

GET reports/{report_id}
UPDATE reports/{report_id}
DELETE reports/{report_id}

Workflow:

Defines a set of possible states and the possible transitions between them.
Workflows can be attached to services.
As a first step a workflow is just a set of states.

POST workflows
Create a new workflow

GET workflows

UPDATE workflows/{workflow_id}
DELETE workflows/{workflow_id}
GET workflows/{workflow_id}
