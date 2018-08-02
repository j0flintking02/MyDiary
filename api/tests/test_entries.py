import unittest
import json
from db import Config, Users, Entries
from api import app





class MyTestCase(unittest.TestCase):
    new_user = [{'user_name': 'john', 'password': '1234'}]

    def setUp(self):
        app.config['TESTING'] = True
        config = Config()
        self.cur = config.cur
        self.app = app.test_client()

    def test_sign_up_user(self):
        resp = self.app.post('/api/v1/auth/signup',
                             data=json.dumps(dict(username="john", password="1234")),
                             content_type="application/json")
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(message="new user created"))

        self.assertEqual(resp.status_code, 201)

    def test_signup_validation(self):
        resp = self.app.post('/api/v1/auth/signup',
                             data=json.dumps(dict(username=" ", password=" ")),
                             content_type="application/json")
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(message="Field must not be empty"))

    def test_login_user(self):
        resp1 = self.app.post('/api/v1/auth/signup',
                              data=json.dumps(dict(username="john", password="1234")),
                              content_type="application/json"
                              )

        resp = self.app.post('/api/v1/auth/login', data=json.dumps({
            "username": "john",
            "password": "1234"
        }), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_entry_list(self):
        """tests for all entries in the data storage"""
        resp1 = self.app.post('/api/v1/auth/signup',
                              data=json.dumps(dict(username="john", password="1234")),
                              content_type="application/json"
                              )

        resp2 = self.app.post('/api/v1/auth/login', data=json.dumps({
            "username": "john",
            "password": "1234"
        }), content_type="application/json")
        data = json.loads(resp2.get_data())
        token = data['token']
        resp = self.app.get('/api/v1/entries', headers={'x-access-token': token}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_single_entry(self):
        """ tests for a single entry """
        self.app.post('/api/v1/auth/signup',
                      data=json.dumps(dict(username="john", password="1234")),
                      content_type="application/json"
                      )

        resp2 = self.app.post('/api/v1/auth/login', data=json.dumps({
            "username": "john",
            "password": "1234"
        }), content_type="application/json")
        data = json.loads(resp2.get_data())
        token = data['token']
        resp3 = self.app.post('/api/v1/entries',
                              data=json.dumps(dict(title='home land',
                                                   description='we all were born for greatness'
                                                   )), headers={'x-access-token': token},
                              content_type="application/json"
                              )

        resp = self.app.get('/api/v1/entries/1',
                            headers={'x-access-token': token},
                            content_type="application/json"
                            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_add_one(self):
        """ tests for adding a single entry """
        resp1 = self.app.post('/api/v1/auth/signup',
                              data=json.dumps(dict(username="john", password="1234")),
                              content_type="application/json"
                              )

        resp2 = self.app.post('/api/v1/auth/login', data=json.dumps({
            "username": "john",
            "password": "1234"
        }), content_type="application/json")
        data = json.loads(resp2.get_data())
        token = data['token']
        resp = self.app.post('/api/v1/entries', data=json.dumps(dict(title='home land',
                                                                     description='we all were born for greatness'
                                                                     )),
                             headers={'x-access-token': token},
                             content_type="application/json"
                             )

        self.assertEqual(resp.content_type, 'application/json')

    def test_edit_one(self):
        """ tests for editing a single entry """
        resp_signup = self.app.post('/api/v1/auth/signup',
                                    data=json.dumps(dict(username="john", password="1234")),
                                    content_type="application/json"
                                    )
        self.assertEqual(resp_signup.status_code, 201)
        resp_login = self.app.post('/api/v1/auth/login', data=json.dumps({
            "username": "john",
            "password": "1234"
        }), content_type="application/json")
        data = json.loads(resp_login.get_data())
        token = data['token']
        self.app.post('/api/v1/entries',
                      data=json.dumps(
                          dict(title='home land',
                               description='we all were born for greatness')),
                      headers={'x-access-token': token},
                      content_type="application/json"
                      )
        resp_edit = self.app.put('/api/v1/entries/1',
                                 data=json.dumps(
                                     dict(title='home land security',
                                          description='we all were born for greatness')
                                 ), headers={'x-access-token': token},
                                 content_type="application/json")
        self.assertEqual(resp_edit.status_code, 200)
        self.assertEqual(resp_edit.content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()
