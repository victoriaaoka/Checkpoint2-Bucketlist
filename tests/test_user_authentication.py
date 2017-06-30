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
        self.user_login = {
            'username': 'vicky',
            'password': 'password'

        }
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """reset all initialized variables."""
        with self.app.app_context():
            db.session.close()
            db.drop_all()

    def test_successful_registration(self):
        """Test successful user registration."""
        response = self.client().post('v1/auth/register', data=json.dumps(
            self.user_data))
        self.assertEqual(response, "You registered successfully!")
        self.assertEqual(response.status_code, 201)

    def test_register_without_username_or_password(self):
        """Test the registration of a user without a username and password."""
        new_user = {
            'email': 'vicky@gmail.com',
            'username': ' ',
            'password': ' '
        }
        response = self.client().post('/auth/register', data=json.dumps(new_user))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response, "Please fill in the required fields.")

    def test_register_with_username_not_string(self):
        """Test the registration of a user with a username that is not string."""
        new_user = {
            'email': 'vicky@gmail.com',
            'username': '@#$$54678',
            'password': 'password'
        }
        response = self.client().post('/auth/register', data=json.dumps(new_user))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response, "The user name can only be a string.")

    def test_register_with_invalid_email(self):
        """Test the registration of a user with an invalid email."""
        new_user = {
            'email': 'vicky5678',
            'username': ' vicky',
            'password': ' password'
        }
        response = self.client().post('/auth/register', data=json.dumps(new_user))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response, "Invalid email address.")

    def test_register_with_short_password(self):
        """Test the registration of a user with a very short password."""
        new_user = {
            'email': 'vicky@gmail.com',
            'username': ' vicky',
            'password': ' pass'
        }
        response = self.client().post('/auth/register', data=json.dumps(new_user))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response, "The password is too short.")

    def test_registering_a_user_who_already_exists(self):
        """Test that a user cannot be registered twice."""
        self.client().post('v1/auth/register', data=json.dumps(self.user_data))
        response = self.client().post('v1/auth/register', data=json.dumps(
            self.user_data))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response['message'], "The user already exists! Please login.")

    def test_registered_user_can_login(self):
        """Test registered user can login successfully."""
        self.client().post('v1/auth/register', data=json.dumps(self.user_data))
        response = self.client().post('v1/auth/login', data=json.dumps(
            self.user_login))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['message'], "You logged in successfully.")
        self.assertTrue(response['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_registered = {
            'username': 'notregistered',
            'password': 'password'
        }

        response = self.client().post('v1/auth/login', data=json.dumps(
            not_registered))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response['message'], "The user does not exist.")

    def test_login_without_username_or_password(self):
        """Test user login without username and password."""
        self.client().post('/auth/register', data=json.dumps(self.user_data))
        response = self.client().post('v1/auth/login', data={
            'username': ' ', 'password': ' '})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response['message'], "Please enter Username and Password.")
        self.assertFalse(response['access_token'])
