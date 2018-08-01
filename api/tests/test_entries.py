import unittest
import json
from db import Config, Users, Entries
from api import app
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import utils
import datetime
import jwt

config = Config()
user_model = Users()
entry_model = Entries()


def sign_up_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    u_id = str(uuid.uuid4())
    user_model.insert_new_user(u_id=u_id, name=username, password=hashed_password)


def login_user(username):
    """login a user"""
    users = user_model.get_all_user()
    output = utils.new_user(users)
    # Check if the values pass through  exist in the database
    check_user = list(filter(lambda output: output['user name'] == username, output))
    token = jwt.encode({'user id': check_user[0]['user id'],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       app.config['SECRET_KEY'])
    return token.decode('UTF-8')


def insert_test_data(date, title, description, author_id):
    entry = entry_model.insert_new_entry(date, title, description, author_id)


class MyTestCase(unittest.TestCase):
    new_user = [{'user_name': 'john', 'password': '1234'}]

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.conn = config.conn
        self.cur = config.conn.cursor()
        self.entry_id = 1

    def test_sign_up_user(self):
        resp = self.app.post('/api/v1/auth/signup',
                             data=json.dumps(dict(user_name="john", password="1234")),
                             content_type="application/json")
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(message="new user created"))

        self.assertEqual(resp.status_code, 201)

    def test_signup_validation(self):
        resp = self.app.post('/api/v1/auth/signup',
                             data=json.dumps(dict(user_name=" ", password=" ")),
                             content_type="application/json")
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(message="Field must not be empty"))

    def test_login_user(self):
        sign_up_user('john', '1234')
        resp = self.app.post('/api/v1/auth/login', data={'username': 'john', 'password': '1234'})
        # self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.content_type, 'application/json')

    def test_entry_list(self):
        """tests for all entries in the data storage"""
        sign_up_user('john', '1234')
        token = login_user('john')
        resp = self.app.get('/api/v1/entries', headers={'x-access-token': token}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_single_entry(self):
        """ tests for a single entry """
        sign_up_user('john', '1234')
        token = login_user('john')
        resp = self.app.get('/api/v1/entries/{}'.format(self.entry_id),
                            headers={'x-access-token': token},
                            content_type="application/json"
                            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_add_one(self):
        """ tests for adding a single entry """
        sign_up_user('john', '1234')
        token = login_user('john')
        resp = self.app.post('/api/v1/entries', data=json.dumps(dict(title='home land',
                                                                     description='we all were born for greatness'
                                                                     )), headers={'x-access-token': token},
                             content_type="application/json"
                             )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.content_type, 'application/json')

    # def test_missing_field(self):
    #     sign_up_user('john', '1234')
    #     token = login_user('john')
    #     resp = self.app.post('/api/v1/entries', data=dict(description='we all were born for greatness'
    #                                                       ), headers={'x-access-token': token})
    #     self.assertEqual(resp.content_type, 'application/json')

    def test_edit_one(self):
        """ tests for editing a single entry """
        sign_up_user('john', '1234')
        token = login_user('john')
        resp = self.app.get('/api/v1/entries/{}'.format(self.entry_id), headers={'x-access-token': token}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()
