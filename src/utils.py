#!/usr/bin/env python3

from typing import Dict, Union
from datetime import datetime
from src.validation_utils import CustomValidator
from src.schema import charging_process_schema
from src.error_utils import create_error_response, abort_with_response


def process_payload(payload: Dict) -> Dict:
    """Processes payload of the request to rate the CDR(s).
    """
    if not isinstance(payload, dict):
        response = create_error_response(
            400,
            'Invalid JSON payload'
        )
        abort_with_response(
            response,
            'process_payload',
            'Request payload must be Dict'
        )

    validator = CustomValidator()
    if not validator.validate(payload, charging_process_schema):
        response = create_error_response(
            422,
            'document contains validation errors',
            validator.errors
        )
        abort_with_response(
            response,
            'process_payload',
            'validation errors in document schema'
        )

    rate = validator.document.get('rate')
    cdr = validator.document.get('cdr')
    return rate_cdr(rate, cdr)


def rate_cdr(
    rate: Dict[str, Union[int, float]], cdr: Dict[str, Union[int, datetime]]
) -> Dict:
    """Applies the given rate to the CDR.
    """
    delivered_energy = cdr.get('meterStop') - cdr.get('meterStart')
    energy_price = (delivered_energy / 1000) * rate.get('energy')
    energy_price = round(energy_price, 3)

    charging_duration = cdr.get('timestampStop') - cdr.get('timestampStart')
    duration_in_hours = charging_duration.total_seconds() / 3600
    time_price = duration_in_hours * rate.get('time')
    time_price = round(time_price, 3)

    service_fee = rate.get('transaction')

    overall = energy_price + time_price + service_fee
    overall_rounded = round(overall, 2)

    return {
        'overall': overall_rounded,
        'components': {
            'energy': energy_price,
            'time': time_price,
            'transaction': service_fee
        }
    }
