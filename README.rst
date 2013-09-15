Taarifa Backend
===============

|Build Status|

Prototype of a Taarifa backend

Installation
------------

`Install MongoDB`_ and run ``mongod`` ::

    mongod

Install python dependencies using pip_ ::

    pip install -r requirements.txt

Start the server ::

    python manage.py runserver

Run the ``curl_send_report`` script from the console to try sending a
report via JSON

API work notes
--------------

The API will support the following requests:

Services:
.........

Defines a report template, i.e. the set of fields which are part of the
report, their type and their contraints. This is comparable to a custom
form.

Create a new service ::

    POST services

List services ::

    GET services

Retrieve / modify / delete service ``service_id`` ::

    GET services/{service_id}
    UPDATE services/{service_id}
    DELETE services/{service_id}

Reports:
........

The collection of information about which a report is made. Must use one
previously defined service.

Create a new report ::

    POST reports

List reports ::

    GET reports

Retrieve / modify / delete report ``report_id`` ::

  GET reports/{report_id}
  UPDATE reports/{report_id}
  DELETE reports/{report_id}

Workflow:
.........

Defines a set of possible states and the possible transitions between
them. Workflows can be attached to services. As a first step a workflow
is just a set of states.

Create a new workflow ::

    POST workflows

List workflows ::

    GET workflows

Retrieve / modify / delete report ``report_id`` ::

    UPDATE workflows/{workflow_id}
    DELETE workflows/{workflow_id}
    GET workflows/{workflow_id}

.. |Build Status| image:: https://travis-ci.org/taarifa/taarifa_backend.png?branch=master
   :target: https://travis-ci.org/taarifa/taarifa_backend
.. _Install MongoDB: http://docs.mongodb.org/manual/installation/
.. _pip: http://www.pip-installer.org/en/latest/requirements.html
