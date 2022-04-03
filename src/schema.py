#!/usr/bin/env python3

from src.schema_utils import str_to_date

charging_process_schema = {
    'rate': {
        'type': 'dict',
        'schema': {
            'energy': {
                'type': 'number',
                'empty': False,
                'required': True,
            },
            'time': {
                'type': 'number',
                'empty': False,
                'required': True,
            },
            'transaction': {
                'type': 'number',
                'empty': False,
                'required': True,
            },
        },
        'required': True,
    },
    'cdr': {
        'type': 'dict',
        'schema': {
            'meterStart': {
                'type': 'integer',
                'min': 0,
                'required': True,
            },
            'timestampStart': {
                'type': 'datetime',
                'empty': False,
                'required': True,
                'coerce': str_to_date,
            },
            'meterStop': {
                'type': 'integer',
                'required': True,
                'check_with': 'meter_start'
            },
            'timestampStop': {
                'type': 'datetime',
                'empty': False,
                'required': True,
                'coerce': str_to_date,
                'check_with': 'timestamp_start'
            },
        },
        'required': True,
    },
}
