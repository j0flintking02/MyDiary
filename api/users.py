from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from api import app
from db import insert_new_user, get_all_user
from config import db_connection as conn
import uuid
import jwt
import datetime
from utils import token_required


app.config['SECRET_KEY'] = 'thisissecret'


@app.route('/api/v1/auth/signup', methods=['POST'])
def sign_up_user():
    """add a new user"""
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    insert_new_user(conn, u_id=str(uuid.uuid4()), name=data['user_name'], password=hashed_password)
    return jsonify({'message': "new user create"})


@app.route('/api/v1/auth/login', methods=['GET'])
def login_user():
    """login a user"""
    users = get_all_user(conn)

    output = []
    for user in users:
        user_data = {'user id': user[1], 'user name': user[2], 'user Password': user[3]}
        output.append(user_data)
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('FAILED TO VERIFY', 401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # Check if the values pass through  exist in the database
    check_user = list(filter(lambda output: output['user name'] == auth.username, output))

    # check if the user exits in the database
    if not (check_user[0]['user name']):
        return make_response('FAILED TO VERIFY', 401,
                             {'WWW-Authenticate': 'Basic realm="Login required"'})
    # check if the user pass is the same
    if check_password_hash(check_user[0]['user Password'], auth.password):
        print(check_user[0]['user Password'])
        token = jwt.encode({'user id': check_user[0]['user id'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('FAILED TO VERIFY', 401,
                         {'WWW-Authenticate': 'Basic realm="Login required"'})


