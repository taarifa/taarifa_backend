#!/usr/bin/env python
import csv
import requests
import json

CSV_FN = 'waterpoints.csv'
REPORTS_URL = 'http://localhost:5000/reports'
SERVICES_URL = 'http://localhost:5000/services'


#simple enum from http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


Status = enum(FUNCTIONAL='functional',
              NOT_FUNCTIONAL='not functional',
              IN_PROGRESS='in progress',
              UNKNOWN='unknown')


class Waterpoint(object):
    #TODO worth it to go through a class?
    def __init__(self, _id, region, lga, ward, village, tech, wptype, status, lat, lon):
        self.waterpoint_id = str(_id)
        self.region = region
        self.lga_name = lga
        self.ward = ward
        self.village = village
        self.technology_in_use = tech
        self.waterpoint = wptype
        self.status = status
        self.latitude = lat
        self.longitude = lon

    def __repr__(self):
        return 'Waterpoint(%s, %s, %s, %s)' % (self.waterpoint_id, self.latitude, self.longitude,
                                               self.status)


def resolve_status(status):
    if status.lower() == "functional":
        return Status.FUNCTIONAL
    elif status.lower() == "not functional":
        return Status.NOT_FUNCTIONAL
    elif status.lower() == "in progress":
        return Status.IN_PROGRESS
    else:
        return Status.UNKNOWN


def parse_csv(csv_fn):
    waterpoints = []
    with open(csv_fn, 'r') as _file:
        reader = csv.reader(_file)
        header = reader.next()
        for _id, row in enumerate(reader):
            d = dict(zip(header, row))

            status = resolve_status(d['STATUS'])

            try:
                lat, lon = float(d['LATITUDE']), float(d['LONGITUDE'])
            except ValueError:
                #TODO log error
                continue

            wp = Waterpoint(_id, *(row[:-3] + [status, lat, lon]))
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
    data = {'service_code': 'wp1', 'data': wp.__dict__}

    requests.post(REPORTS_URL, data=json.dumps(data), headers=headers)


if __name__ == '__main__':
    create_wp_service()
    waterpoints = parse_csv(CSV_FN)
    for w in waterpoints:
        print w
        send_report(w)
