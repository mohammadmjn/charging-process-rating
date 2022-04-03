import json
import sys
from server import app
from typing import Dict
from unittest import TestCase
from werkzeug.test import TestResponse


def parse_response(response: TestResponse) -> Dict:
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))


class TestApiIntegration(TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()

    def rate_charging_process(self, input_data: Dict) -> TestResponse:
        return self.app.post('/rate', json=input_data)

    def test_rate_charging_process_with_empty_body(self):
        input_body = {}
        response = parse_response(self.rate_charging_process(input_body))

        self.assertEqual(response['_error']['code'], 400)
        self.assertEqual(response['_error']['name'], 'Bad Request')
        self.assertEqual(response['_error']['message'], 'Empty JSON body')

    def test_rate_charging_process_with_invalid_json_body(self):
        input_body = '{""""""}'
        response = parse_response(self.rate_charging_process(input_body))

        self.assertEqual(response['_error']['code'], 400)
        self.assertEqual(response['_error']['name'], 'Bad Request')
        self.assertEqual(response['_error']['message'], 'Invalid JSON payload')

    def test_rate_charging_process_with_list_body(self):
        input_body = [{
            'rate': {
                'energy': 0.3,
                'time': 2,
                'transaction': 1
            },
            'cdr': {
                'meterStart': 1204307,
                'timestampStart': '2021-04-05T10:04:00Z',
                'meterStop': 1215230,
                'timestampStop': '2021-04-05T11:27:00Z'
            }
        }]
        response = parse_response(self.rate_charging_process(input_body))

        self.assertEqual(response['_error']['code'], 400)
        self.assertEqual(response['_error']['name'], 'Bad Request')
        self.assertEqual(response['_error']['message'], 'Invalid JSON payload')

    def test_rate_charging_process_without_energy(self):
        input_body = {
            'rate': {
                'time': 2,
                'transaction': 1
            },
            'cdr': {
                'meterStart': 1204307,
                'timestampStart': '2021-04-05T10:04:00Z',
                'meterStop': 1215230,
                'timestampStop': '2021-04-05T11:27:00Z'
            }
        }
        response = parse_response(self.rate_charging_process(input_body))

        self.assertEqual(response['_error']['code'], 422)
        self.assertEqual(response['_error']['name'], 'Unprocessable Entity')
        self.assertEqual(response['_error']['message'], 'document contains validation errors')
        self.assertNotEqual(response.get('_issues'), None)

    def test_rate_charging_process_with_wrong_type_energy(self):
        input_body = {
            'rate': {
                'energy': '0.3',
                'time': 2,
                'transaction': 1
            },
            'cdr': {
                'meterStart': 1204307,
                'timestampStart': '2021-04-05T10:04:00Z',
                'meterStop': 1215230,
                'timestampStop': '2021-04-05T11:27:00Z'
            }
        }
        response = parse_response(self.rate_charging_process(input_body))

        expected_issues = {
            'rate': [{'energy': ['must be of number type']}]
        }

        self.assertEqual(response['_error']['code'], 422)
        self.assertEqual(response['_error']['name'], 'Unprocessable Entity')
        self.assertEqual(response['_error']['message'], 'document contains validation errors')
        self.assertEqual(response.get('_issues'), expected_issues)

    def test_rate_charging_process_without_rate(self):
        input_body = {
            'cdr': {
                'meterStart': 1204307,
                'timestampStart': '2021-04-05T10:04:00Z',
                'meterStop': 1215230,
                'timestampStop': '2021-04-05T11:27:00Z'
            }
        }
        response = parse_response(self.rate_charging_process(input_body))

        expected_issues = {'rate': ['required field']}

        self.assertEqual(response['_error']['code'], 422)
        self.assertEqual(response['_error']['name'], 'Unprocessable Entity')
        self.assertEqual(response['_error']['message'], 'document contains validation errors')
        self.assertEqual(response.get('_issues'), expected_issues)

    def test_rate_charging_process_with_wrong_datetime_format(self):
        input_body = {
            'rate': {
                'energy': 0.3,
                'time': 2,
                'transaction': 1
            },
            'cdr': {
                'meterStart': 1204307,
                'timestampStart': '2021-04-05 10:04:00 GMT',
                'meterStop': 1215230,
                'timestampStop': '2021-04-05T11:27:00Z'
            }
        }
        response = parse_response(self.rate_charging_process(input_body))

        expected_issues = {
            'cdr': [{
                'timestampStart': [
                    'must be of datetime type',
                    "field 'timestampStart' cannot be coerced: time "
                    "data '2021-04-05 10:04:00 GMT' does not match "
                    "format '%Y-%m-%dT%H:%M:%SZ'"
                ]
            }]
        }

        self.assertEqual(response['_error']['code'], 422)
        self.assertEqual(response['_error']['name'], 'Unprocessable Entity')
        self.assertEqual(response['_error']['message'], 'document contains validation errors')
        self.assertEqual(response.get('_issues'), expected_issues)

    def test_rate_charging_process_successful(self):
        input_body = {
            'rate': {
                'energy': 0.3,
                'time': 2,
                'transaction': 1
            },
            'cdr': {
                'meterStart': 1204307,
                'timestampStart': '2021-04-05T10:04:00Z',
                'meterStop': 1215230,
                'timestampStop': '2021-04-05T11:27:00Z'
            }
        }
        response = parse_response(self.rate_charging_process(input_body))

        expected_response = {
            'overall': 7.04,
            'components': {'energy': 3.277, 'time': 2.767, 'transaction': 1}
        }

        self.assertEqual(response, expected_response)
