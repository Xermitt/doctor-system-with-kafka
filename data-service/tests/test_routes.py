import unittest
from data_service.src.app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_search_no_params(self):
        response = self.app.get('/api/search')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()