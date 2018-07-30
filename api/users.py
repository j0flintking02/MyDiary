from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from api import app
import db
import utils
from config import db_connection as conn
import uuid
import jwt
import datetime


app.config['SECRET_KEY'] = 'thisissecret'


@app.route('/api/v1/auth/signup', methods=['POST'])
def sign_up_user():
    """add a new user"""
    data = request.get_json()
    name = data['user_name']
    password = data['password']
    # check if the user entered all fields
    if name is not ' ' and password is not ' ':
        hashed_password = generate_password_hash(password, method='sha256')
        u_id = str(uuid.uuid4())
        db.insert_new_user(conn, u_id=u_id, name=name, password=hashed_password)
        return jsonify({'message': "new user create"})

    return jsonify({'message': "Field must not be empty"})


@app.route('/api/v1/auth/login', methods=['GET'])
def login_user():
    """login a user"""
    users = db.get_all_user(conn)
    output = utils.new_user(users)
    auth = request.authorization

    # check if the user entered all credentials
    if not auth or not auth.username or not auth.password:
        return make_response('FAILED TO VERIFY', 401,
                             {'WWW-Authenticate': 'Basic realm="User must login!"'})

    # Check if the values pass through  exist in the database
    check_user = list(filter(lambda output: output['user name'] == auth.username, output))

    # check if the user exits in the database
    if not (check_user[0]['user name']):
        return make_response('FAILED TO VERIFY', 401,
                             {'WWW-Authenticate': 'Basic realm="Login required"'})
    # check if the user pass is the same
    if check_password_hash(check_user[0]['user Password'], auth.password):
        token = jwt.encode({'user id': check_user[0]['user id'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('FAILED TO VERIFY', 401,
                         {'WWW-Authenticate': 'Basic realm="Login required"'})





