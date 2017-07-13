import json
import unittest
from tests.base import BaseTestCase


class AuthTestCase(BaseTestCase):
    """Test case for the authentication blueprint."""

    def test_successful_registration(self):
        """Test successful user registration."""
        new_user = {
            'email': 'vicky@gmail.com',
            'username': ' vicky',
            'password': ' password'
        }
        response = self.client().post(
            '/api/v1/auth/register', data=new_user)
        self.assertEqual(response.status_code, 201)

    def test_register_without_username_or_password(self):
        """Test the registration of a user without a username and password."""
        new_user = {
            'email': 'vicky@gmail.com',
            'username': ' ',
            'password': ' '
        }
        response = self.client().post(
            '/api/v1/auth/register', data=json.dumps(new_user))
        self.assertEqual(response.status_code, 400)

    def test_register_with_username_not_string(self):
        """
        Test the registration of a user with a
        username that is not string.
        """
        new_user = {
            'email': 'vicky@gmail.com',
            'username': '@#$$54678',
            'password': 'password'
        }
        response = self.client().post('/api/v1/auth/register', data=json.dumps(
            new_user))
        self.assertEqual(response.status_code, 400)

    def test_register_with_invalid_email(self):
        """Test the registration of a user with an invalid email."""
        new_user = {
            'email': 'vicky5678',
            'username': ' vicky',
            'password': ' password'
        }
        response = self.client().post(
            '/api/v1/auth/register', data=json.dumps(new_user))
        self.assertEqual(response.status_code, 400)

    def test_register_with_short_password(self):
        """Test the registration of a user with a very short password."""
        new_user = {
            'email': 'vicky@gmail.com',
            'username': ' vicky',
            'password': ' pas'
        }
        response = self.client().post(
            'api/v1/auth/register', data=json.dumps(new_user))
        self.assertEqual(response.status_code, 400)

    def test_registering_a_user_who_already_exists(self):
        """Test that a user cannot be registered twice."""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        response = self.client().post(
            '/api/v1/auth/register', data=self.user_data)
        self.assertEqual(response.status_code, 409)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['message'], 'The username has been taken.')

    def test_registered_user_can_login(self):
        """Test registered user can login successfully."""
        self.client().post('/api/v1/auth/register', data=self.user_data)
        response = self.client().post(
            '/api/v1/auth/login', data=self.user_login)
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertEqual(output['message'], 'You logged in successfully.')
        self.assertTrue(output['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        not_registered = {
            'username': 'notregistered',
            'password': 'password'
        }

        response = self.client().post(
            '/api/v1/auth/login', data=not_registered)
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['message'], 'Invalid username \
or password, Please try again.')

    def test_login_without_username_or_password(self):
        """Test user login without username and password."""
        response = self.client().post('/api/v1/auth/login', data={
            'username': ' ', 'password': ''})
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode())
