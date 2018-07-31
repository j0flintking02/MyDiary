from functools import wraps
from flask import jsonify, request
import jwt
from api import app
from db import Users


user_model = Users()


def token_required(f):
    """ creating a token decorator that is to be inserted to all end routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        """function to return the user token """
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            users = user_model.get_all_user()
            output = []
            for user in users:
                user_data = {'user id': user[1], 'user name': user[2], 'user Password': user[3]}
                output.append(user_data)
            # Check if the values passed through  exist in the database
            logged_in_user = list(filter(lambda output: output['user id'] == data['user id'],
                                         output))
            current_user = logged_in_user[0]['user id']
        except:
            return jsonify({'message': 'invalid token 1'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


def entry(entries):
    """A function to return a list entry objects"""
    output = []
    for entry in entries:
        user_data = {'entry id': entry[0], ' entry date': entry[1], 'title': entry[2], 'description': entry[3]}
        output.append(user_data)
    return output


def new_user(users):
    """A list to return the list of users from the database"""
    output = []
    for user in users:
        user_data = {'user id': user[1], 'user name': user[2], 'user Password': user[3]}
        output.append(user_data)
    return output