import requests
import json

def send_report():
    url = 'http://localhost:5000/reports'
    headers = {'content-type': 'application/json'}
    data = {'service_code': 'wp001',
            'data': {'functional': True,
                     'latitude': 3.12121,
                     'longitude': 3.42,
                     'waterpoint_id': 'WP_LOC_CODE_001',
                     }
            }

    requests.post(url, data=json.dumps(data), headers=headers)

if __name__ == '__main__':
    send_report()

