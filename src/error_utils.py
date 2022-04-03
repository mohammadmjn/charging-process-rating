#!/usr/bin/env python3

import json
from typing import Union, Dict
from werkzeug.http import HTTP_STATUS_CODES
from flask import Response, abort, current_app


def abort_with_response(
    response: Response, func_name: str, log_message: str
) -> None:
    """Raises an HTTPException with the given response object and
    logs the details of the exception.
    """
    current_app.logger.error('{}: {}'.format(func_name, log_message))
    abort(response)


def create_error_response(
    status_code: int, error_message: str, issues: Union[Dict, None] = None
) -> Response:
    """Creates a response object for the HTTP exception
    """
    if not issues:
        response_body = {
            '_status': 'ERR',
            '_error': {
                'code': status_code,
                'name': HTTP_STATUS_CODES.get(status_code, 'Unknown Error'),
                'message': error_message
            }
        }
    else:
        response_body = {
            '_status': 'ERR',
            '_issues': issues,
            '_error': {
                'code': status_code,
                'name': HTTP_STATUS_CODES.get(status_code, 'Unknown Error'),
                'message': error_message
            }
        }

    json_response = json.dumps(response_body)

    return Response(
        response=json_response,
        status=status_code,
        mimetype='application/json',
    )
