import unittest
import json
from my_app import create_app, db


class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables and app-."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user_data = {
            'username': 'vicky',
            'email': 'v@gmail.com',
            'password': 'password'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_successful_registration(self):
        """Test successful user registration."""
        response = self.client().post('/auth/register', data=self.user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "You registered successfully!")
        self.assertEqual(response.status_code, 201)

    def test_registering_a_user_who_already_exists(self):
        """Test that a user cannot be registered twice."""
        response = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(response.status_code, 201)
        second_response = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_response.status_code, 202)
        result = json.loads(second_response.data.decode())
        self.assertEqual(
            result['message'], "The user already exists! Please login.")
