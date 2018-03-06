import json
import unittest
from my_app.app import create_app, db


class BaseTestCase(unittest.TestCase):

    def setUp(self):
            """Set up test variables and app-."""
            self.app = create_app(config_name='testing')
            self.client = self.app.test_client
            self.bucketlist = {'name': 'Vacation'}
            self.bucketlist_item = {'name': 'Go to Tokyo', 'done': False}
            self.user_data = {
                'username': 'vicky',
                'email': 'v@gmail.com',
                'password': 'password'
            }
            self.user_login = {
                'username': 'vicky',
                'password': 'password'

            }
            self.cntx = self.app.app_context()
            self.cntx.push()
            db.create_all()

            self.client().post('/api/v1/auth/register', data=self.user_data)

    def tearDown(self):
        """reset all initialized variables."""
        with self.app.app_context():
            db.session.close()
            db.drop_all()

    def get_token(self):
        """Return authentication token."""
        response = self.client().post(
            '/api/v1/auth/login', data=self.user_login)
        output = json.loads(response.data.decode())
        token = output['access_token']
        return {'access_token': token}
