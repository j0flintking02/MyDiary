from flask import jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from api import app
from db import Users
import utils
import uuid
import jwt
import datetime

user_model = Users()

app.config['SECRET_KEY'] = 'thisissecret'


@app.route('/api/v1/auth/signup', methods=['POST'])
def sign_up_user():
    """
    Return back the a successful message.
    ---
    parameters:
      - in: body
        username: body
        description: JSON parameters.
        schema:
          properties:
            username:
              type: string
              description: user name that is used during login.
              example: flintking
            password:
              type: string
              description: password for accessing the entries.
              example: password123
    responses:
      201:
        description: OK.
    """
    data = request.get_json()
    name = data['username']
    password = data['password']
    # check if the user entered all fields
    if name is not ' ' and password is not ' ':
        if name.isalpha():
            hashed_password = generate_password_hash(password, method='sha256')
            u_id = str(uuid.uuid4())
            users = user_model.get_all_user()
            output = utils.new_user(users)

            # check if the username already exits
            check_user = list(filter(lambda output: output['user name'] == name, output))
            print(check_user)
            if check_user == []:
                user_model.insert_new_user(u_id=u_id, name=name, password=hashed_password)
                return jsonify({'message': "new user created"}), 201
            else:
                return jsonify({'message': 'username is already taken'}), 400
        else:
            return jsonify({'message': 'you can not have symbols for a name'}), 400

    return jsonify({'message': "Field must not be empty"})


@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():

    users = user_model.get_all_user()
    output = utils.new_user(users)
    auth = request.get_json()

    # check if the user entered all credentials
    if not auth or not auth['username'] or not auth['password']:
        return make_response(jsonify({'message': 'failed to verify'}), 401)
    # Check if the values pass through  exist in the database
    check_user = list(filter(lambda output: output['user name'] == auth['username'], output))
    print(check_user)
    # check if the user exits in the database
    if check_user != []:
        if not (check_user[0]['user name']):
            return make_response(jsonify({'message': 'failed to verify'}), 401)
        # check if the user pass is the same
        if check_password_hash(check_user[0]['user Password'], auth['password']):
            token = jwt.encode({'user id': check_user[0]['user id'],
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                               app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'check': "there is something wrong with your login"})
