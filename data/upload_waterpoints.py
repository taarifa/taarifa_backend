#!/usr/bin/env python
import csv
import requests
import json

CSV_FN = 'waterpoints.csv'
REPORTS_URL = 'http://localhost:5000/reports'
SERVICES_URL = 'http://localhost:5000/services'


class Status(object):
    FUNCTIONAL, NOT_FUNCTIONAL, IN_PROGRESS, UNKNOWN = range(4)


def resolve_status(status):
    if status.lower().startswith("functional"):
        return Status.FUNCTIONAL
    elif status.lower().startswith("not functional") or \
            status.lower().startswith("non functional"):
        return Status.NOT_FUNCTIONAL
    elif status.lower() == "in progress":
        return Status.IN_PROGRESS
    else:
        return Status.UNKNOWN


def parse_csv(csv_fn):
    waterpoints = []
    with open(csv_fn, 'r') as f:
        reader = csv.reader(f)
        header = [field.lower().replace(' ', '_')
                  for field in reader.next()]
        for _id, row in enumerate(reader):
            wp = dict(zip(header, row))
            wp['waterpoint_id'] = _id
            wp['status'] = resolve_status(wp['status'])

            try:
                wp['latitude'] = float(wp['latitude'])
                wp['longitude'] = float(wp['longitude'])
            except ValueError:
                # TODO log error
                continue

            waterpoints.append(wp)

    return waterpoints


def create_wp_service():
    headers = {'content-type': 'application/json'}
    data = {'name': 'WaterpointService',
            'fields': {'waterpoint_id': {'type': 'StringField', 'required': True},
                       'region': {'type': 'StringField', 'required': True},
                       'lga_name': {'type': 'StringField', 'required': True},
                       'ward': {'type': 'StringField', 'required': True},
                       'village': {'type': 'StringField', 'required': True},
                       'technology_in_use': {'type': 'StringField', 'required': True},
                       'waterpoint': {'type': 'StringField', 'required': True},
                       'status': {'type': 'StringField', 'required': True},
                       'latitude': {'type': 'FloatField', 'required': True},
                       'longitude': {'type': 'FloatField', 'required': True},
                       },
            'group': 'location based reports',
            'keywords': ['waterpoints'],
            'protocol_type': '',
            'service_name': '',
            'service_code': 'wp1'
            }
    requests.post(SERVICES_URL, data=json.dumps(data), headers=headers)


def send_report(wp):
    headers = {'content-type': 'application/json'}
    data = {'service_code': 'wp1', 'data': wp}

    requests.post(REPORTS_URL, data=json.dumps(data), headers=headers)


if __name__ == '__main__':
    create_wp_service()
    waterpoints = parse_csv(CSV_FN)
    for w in waterpoints:
        print w
        send_report(w)
