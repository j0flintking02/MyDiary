import unittest
import json
from api import app


class MyTestCase(unittest.TestCase):
    data = [{'date': "21/07/2017", 'description': 'lorem ipsum', 'entry_id': 1, 'title': 'jonathan in never land'},
            {'date': "21/07/2017", 'description': 'lorem ipsum', 'entry_id': 1, 'title': 'jonathan in never land'}]

    def setUp(self):
        self.app = app.test_client()
        self.entry_id =[1,2]

    def test_entry_list(self):
        """tests for all entries in the data storage"""
        resp = self.app.get('/api/v1/entries')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

    def test_single_entry(self):
        """ tests for a single entry """
        resp = self.app.get('/api/v1/entries/{}'.format(self.data[1]['entry_id']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(entry=dict(date="21/07/2017", description='lorem ipsum', entry_id=1,
                                                  title='jonathan in never land')))

    def test_add_one(self):
        """ tests for adding a single entry """
        resp = self.app.post('/api/v1/entries', data=json.dumps(self.data[0]),
                             content_type='application/json')
        self.assertEqual(resp.status_code, 201)

    def test_edit_one(self):
        """ tests for editing a single entry """
        resp = self.app.put('/api/v1/entries/1', data=json.dumps(dict(description='lorem ipsum',
                            title='jonathan in never land')),content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_delete_one(self):
        """ tests for deleting a single entry """
        resp = self.app.get('/api/v1/entries/2')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        content = json.loads(resp.get_data())
        self.assertEqual(content, dict(entry=dict(date='21/07/2017', description='lorem ipsum', entry_id=2,
                                                  title='jonathan in never land')))


if __name__ == '__main__':
    unittest.main()
