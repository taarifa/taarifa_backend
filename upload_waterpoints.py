#!/usr/bin/env python
import csv
import requests
import json

CSV_FN = 'waterpoints.csv'
REPORTS_URL = 'http://localhost:5000/reports'
class Waterpoint(object):
    def __init__(self, _id, lat, _long, functional):
        self.id = str(_id)
        self.lat = lat
        self.long = _long
        self.functional = functional
    def __repr__(self):
        return 'Waterpoint(%s, %s, %s, %s)' % (self.id, self.lat, self.long,
            self.functional)


def parse_csv(csv_fn):
    waterpoints = []
    _id = 0
    with open(csv_fn, 'r') as _file:
        reader = csv.reader(_file)
        header = reader.next()
        for row in reader:
            d = dict(zip(header, row))
            status = d['STATUS']
            if status not in ['Not functional', 'Functional']:
                continue
            functional = status == 'Functional'
            try:
                _lat, _long = float(d['LATITUDE']), float(d['LONGITUDE'])
            except ValueError as e:
                continue
            waterpoints.append(Waterpoint(_id, _lat, _long, functional))
            _id += 1
    return waterpoints

def send_report(wp):
    headers = {'content-type': 'application/json'}
    data = {'service_code': 'wp001',
            'data': {'functional': wp.functional,
                     'latitude': wp.lat,
                     'longitude': wp.long,
                     'waterpoint_id': wp.id,
                     }
            }

    requests.post(REPORTS_URL, data=json.dumps(data), headers=headers)


if __name__ == '__main__':
    waterpoints = parse_csv(CSV_FN)
    for w in waterpoints:
        print w
        send_report(w)


