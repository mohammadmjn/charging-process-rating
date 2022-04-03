#!/usr/bin/env python3

from cerberus import Validator
from datetime import datetime


class CustomValidator(Validator):
    def _check_with_meter_start(self, field, value):
        """ {'type': 'boolean'} """
        meter_start = self.document.get('meterStart')
        if meter_start is not None and value and isinstance(value, int) and \
                value < meter_start:
            self._error(field, 'Min value is {}'.format(meter_start))

    def _check_with_timestamp_start(self, field, value):
        """ {'type': 'boolean'} """
        timestamp_start = self.document.get('timestampStart')
        if timestamp_start is not None and value and isinstance(value, datetime) and \
                isinstance(timestamp_start, datetime) and value < timestamp_start:
            self._error(field, 'Min datetime value is {}'.format(timestamp_start))
