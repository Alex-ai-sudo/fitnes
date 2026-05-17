from flask import Blueprint, request, jsonify, send_from_directory
from .dialog import dialog
import logging

bp = Blueprint('main', __name__)

storage = {}

@bp.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    dialog(request.json, response, storage)

    logging.info('Response: %r', response)
    return jsonify(response)


@bp.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)