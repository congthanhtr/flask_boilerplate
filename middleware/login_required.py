from functools import wraps
from flask import jsonify, request
import datetime

from ..module.auth.model import User


def login_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            payload = User.decode_token(token)
            exp = payload.get('exp')
            if exp < datetime.datetime.utcnow().timestamp():
                return jsonify({'message': 'Token expired'}), 401
            return fn(*args, **kwargs)
        else:
            return jsonify({'message' : 'Token is missing !!'}), 401
    return decorated
