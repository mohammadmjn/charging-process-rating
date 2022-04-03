#!/usr/bin/env python3

import os
import json
import logging
from flask_cors import CORS
from flask import Blueprint, request, Response
from logging.handlers import RotatingFileHandler
from src.error_utils import create_error_response, abort_with_response
from src.utils import process_payload

api = Blueprint('api', __name__)

# Allow the incoming requests to access the endpoints
CORS(api)

MAX_LOG_FILE_BYTES = 5 << 20
MAX_LOG_FILE_BACKUP = 9


def init_logging():
    handler = RotatingFileHandler(
        os.environ.get('RUNTIME_LOG'),
        maxBytes=MAX_LOG_FILE_BYTES,
        backupCount=MAX_LOG_FILE_BACKUP
    )
    logger = logging.getLogger('werkzeug')
    logger.addHandler(handler)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)


@api.route('/rate', methods=['POST'])
def rate_charging_process():
    payload = request.get_json()
    if not payload:
        response = create_error_response(400, 'Empty JSON body')
        abort_with_response(response, 'rate_charging_process', 'Empty JSON body')

    response_body = process_payload(payload)
    return Response(response=json.dumps(response_body),
                    status=200,
                    mimetype='application/json')
