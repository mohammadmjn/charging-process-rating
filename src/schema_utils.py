#!/usr/bin/env python3

from datetime import datetime

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def str_to_date(datetime_str):
    """Converts a date string formatted in ISO 8601
    to the corresponding datetime value.
    """
    return datetime.strptime(datetime_str, DATE_FORMAT) if datetime_str else None
