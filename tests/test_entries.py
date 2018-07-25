import unittest
import json
from api import app


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.entry_id = 1

    def test_entry_list(self):
        """tests for all entries in the data storage"""
        resp = self.app.get('/api/v1/entries')
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
