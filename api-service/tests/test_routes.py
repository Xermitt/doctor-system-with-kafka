import unittest
from api_service.src.app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_appointment_missing_fields(self):
        response = self.app.post('/api/appointment', json={"patient_name": "Test"})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

if __name__ == '__main__':
    unittest.main()