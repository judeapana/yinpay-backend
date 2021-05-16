from flask import make_response, jsonify, request, current_app


def flash(message):
    return make_response(jsonify(message=message))


def get_uuid():
    with current_app.app_context():
        return request.path.split('/')[-1] or None
