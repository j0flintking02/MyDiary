import unittest
import json
from .app import app as app_step


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app_step.test_client()
        self.entry_id = 1

    def test_entry_list(self):
        resp = self.app.get('/api/v1/entries')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0], {
            'entry_id': 1,
            'title': 'jonathan in never land',
            'description': 'lorem ipsum'
        })

    def test_single_entry(self):
        resp = self.app.get('/api/v1/entries/<int:{}>'.format(self.entry_id))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')

        content = json.loads(resp.get_data(as_text=True))
        self.assertEqual(content, {
            'entry_id': 1,
            'title': 'jonathan in never land',
            'description': 'lorem ipsum'
        })

    # def test_book_detail_404(self):
    #     resp = self.app.get('/entry_id/1111')
    #     self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
