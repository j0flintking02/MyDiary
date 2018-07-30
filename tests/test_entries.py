import unittest
import json
from config import db_connection as conn
from api import app


class MyTestCase(unittest.TestCase):
    new_user = [{'user_name': 'john', 'password': '1234'}]

    def setUp(self):
        self.app = app.test_client()
        self.conn = conn
        self.cur = conn.cursor()
        self.entry_id = 1

    def test_sign_up_user(self):
        print(self.new_user[0])
        resp = self.app.post('/api/v1/auth/signup', data=json.dumps(dict(user_name="john", password="1234")))
        sql = """INSERT INTO my_diary.public.users(user_id, user_name,user_password)VALUES(%s,%s,%s);"""
        u_id = "fbe00936-d8be-48db-9ba6-a12550576fb2"
        self.cur.execute(sql, (u_id,  "john", '1234'))
        self.assertEqual(resp.status_code, 201)

    def test_index(self):
        resp = self.app.get('/', data=json.dumps(dict(message="Welcome to the entry port")))
        self.assertEqual(resp.status_code, 200)

    def test_entry_list(self):
        """tests for all entries in the data storage"""
        resp = self.app.get('/api/v1/entries',
                            headers={"x-access-token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIGlkIjoiZDF"
                                                       "jYmQ3NmEtMmZhZS00NzZkLTliZGMtOWU2NjMyMDlmMDEzIiwiZXhwIjox"
                                                       "NTMyNzY5NjQzfQ.7CE9srHSrkWucF8kvwhZMsnGBLD0H0U1ZH9dTWoqMwg"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_single_entry(self):
        """ tests for a single entry """
        resp = self.app.get('/api/v1/entries/{}'.format(self.entry_id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(entry=dict(date="21/07/2017", description='lorem ipsum', entry_id=1,
                                                  title='jonathan in never land')))

    def test_add_one(self):
        """ tests for adding a single entry """
        resp = self.app.get('/api/v1/entries')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.content_type, 'application/json')

    def test_edit_one(self):
        """ tests for editing a single entry """
        resp = self.app.get('/api/v1/entries/{}'.format(self.entry_id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(entry=dict(date="21/07/2017", description='lorem ipsum', entry_id=1,
                                                  title='jonathan in never land')))

    def test_delete_one(self):
        """ tests for deleting a single entry """
        resp = self.app.get('/api/v1/entries/{}'.format(self.entry_id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(entry=dict(date='21/07/2017', description='lorem ipsum', entry_id=1,
                                                  title='jonathan in never land')))


if __name__ == '__main__':
    unittest.main()
