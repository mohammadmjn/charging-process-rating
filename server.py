#!/usr/bin/env python3

import os
import json
from flask import Flask, Response
from werkzeug.exceptions import HTTPException
from src.api import api, init_logging

app = Flask(__name__)
app.register_blueprint(api)

MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH'))
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH * 1024

init_logging()


@app.errorhandler(HTTPException)
def handle_exception(error: HTTPException) -> Response:
    """Return JSON instead of HTML for HTTP errors."""
    response = error.get_response()
    response.data = json.dumps({
        '_status': 'ERR',
        '_error': {
            'code': error.code,
            'name': error.name,
            'message': error.description
        }
    })
    response.content_type = 'application/json'
    return response


if __name__ == '__main__':
    app.run()
