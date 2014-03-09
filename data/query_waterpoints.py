#!/usr/bin/env python
import requests
import json


def get_all_reports():
    url = 'http://localhost:5000/reports'
    params = {'service_code': 'wp001'}

    response = requests.get(url, params=params)
    print response.url
    print response.ok

    reports = json.loads(response.text)
    for r in reports:
        print r
    print 'Total %s reports' % len(reports)

if __name__ == '__main__':
    get_all_reports()
