import unittest
import json
from db import Config
from api import app

config = Config()


class MyTestCase(unittest.TestCase):
    new_user = [{'user_name': 'john', 'password': '1234'}]

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.conn = config.conn
        self.cur = config.conn.cursor()
        self.entry_id = 1

    def test_sign_up_user(self):
        resp = self.app.post('/api/v1/auth/signup', data=json.dumps(dict(user_name="john", password="1234")),
                             content_type="application/json")
        self.assertEqual(resp.status_code, 201)

    def test_index(self):
        resp = self.app.get('/', data=json.dumps(dict(message="Welcome to the entry port")))
        self.assertEqual(resp.status_code, 200)

    def test_login_user(self):
        resp = self.app.get('/api/v1/auth/login', data=json.dumps(dict(user_name="john", password="1234")))
        # self.assertEqual(resp.status_code, 200)

    def test_entry_list(self):
        """tests for all entries in the data storage"""
        resp = self.app.get('/api/v1/entries')
        self.assertEqual(resp.content_type, 'application/json')

    def test_single_entry(self):
        """ tests for a single entry """
        resp = self.app.get('/api/v1/entries/{}'.format(self.entry_id))
        self.assertEqual(resp.content_type, 'application/json')

    def test_add_one(self):
        """ tests for adding a single entry """
        resp = self.app.get('/api/v1/entries')
        self.assertEqual(resp.content_type, 'application/json')

    def test_edit_one(self):
        """ tests for editing a single entry """
        resp = self.app.get('/api/v1/entries/{}'.format(self.entry_id))
        self.assertEqual(resp.content_type, 'application/json')


if __name__ == '__main__':
    unittest.main()
