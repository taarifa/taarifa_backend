#!/usr/bin/env python
import requests
import json


def get_all_reports():
    url = 'http://localhost:5000/reports'
    params = {'service_code': 'wp001'}

    response = requests.get(url, params=params)
    print response.url
    print response.ok

    data = json.loads(response.text)
    reports = data['result']
    print reports[0]
    print len(reports)

if __name__ == '__main__':
    get_all_reports()
