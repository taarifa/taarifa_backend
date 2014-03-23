TEST_DB = 'taarifa_backend_test'
if __name__ == '__main__':
    # setup the environment variable to use a test database when run from the command line
    import os
    os.environ['DBNAME'] = TEST_DB

import json
from taarifa_backend import app, db
import unittest

REPORTS_URL = '/reports'
SERVICE_URL = '/services'
SERVICE_CODE = "test0001"
SUCESS = '200 OK'

SERVICE_DESC = {"classname": "TestReport",
                "fields": [{"name": "title", "fieldtype": "StringField", "max_length": 255, "required": True},
                           {"name": "desc", "fieldtype": "StringField", "required": True}],
                "description": "report create from create_service test",
                "keywords": ["location", "report"],
                "group": "location based reports",
                "service_name": "test report",
                "service_code": SERVICE_CODE,
                }

REPORT_DATA = {'service_code': SERVICE_CODE,
               'data': {'title': 'Test report',
                        'latitude': 70,
                        'longitude': 20,
                        'desc': 'report send from test_api.py',
                        }
               }

logger = app.logger


class ApiTest(unittest.TestCase):

    def setUp(self):
        # Somehow it is not so easy to find out which database is used
        # this assert at least makes sure the app config is set to the test_db
        configured_db = app.config['MONGODB_SETTINGS']['db']
        assert configured_db == TEST_DB, 'Expected to use %s as a db, but was configured to use %s' % (TEST_DB, configured_db)
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        db.connection.drop_database(TEST_DB)

    def test_call_landing_page(self):
        self.app.post('/')

    def test_create_service_and_post_report_and_query_reports(self):
        self._create_service()
        self._query_services()
        report_id = self._post_report()
        logger.debug('Posted report with report id: ' + report_id)
        self._get_report(report_id)
        self._get_all_reports()

    def _create_service(self):
        result = self.app.post(SERVICE_URL, data=json.dumps(SERVICE_DESC), content_type='application/json')
        self._check_status_and_log(result)

    def _query_services(self):
        result = self.app.get(SERVICE_URL)
        self._check_status_and_log(result)

    def _post_report(self):
        result = self.app.post(REPORTS_URL, data=json.dumps(REPORT_DATA), content_type='application/json')
        self._check_status_and_log(result)
        return json.loads(result.data)['_id']['$oid']

    def _get_report(self, report_id):
        result = self.app.get(REPORTS_URL + '/%s' % report_id)
        self._check_status_and_log(result)

    def _get_all_reports(self):
        result = self.app.get(REPORTS_URL + '?service_code=%s' % SERVICE_CODE)
        self._check_status_and_log(result)

    def _check_status_and_log(self, result):
        self.assertEqual(result._status, SUCESS)
        #TODO: should put some validation of the data here
        _json = json.loads(result.data)
        logger.debug(_json)


if __name__ == '__main__':
    unittest.main()
