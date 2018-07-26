from flask import jsonify, request, make_response
from functools import wraps
from api import app
import jwt
from config import db_connection as conn
from db import insert_new_user, get_all_user


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            users = get_all_user(conn)
            output = []
            for user in users:
                user_data = {'user id': user[1], 'user name': user[2], 'user Password': user[3]}
                output.append(user_data)
            # Check if the values passed through  exist in the database
            logged_in_user = list(filter(lambda output: output['user id'] == data['user id'], output))
            current_user = logged_in_user[0]['user id']

        except:
            return jsonify({'message': 'invalid token'}), 401
        return f(current_user, *args, **kwargs)

    return decorated
