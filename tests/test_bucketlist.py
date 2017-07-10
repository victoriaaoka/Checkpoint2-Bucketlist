import unittest
import os
import sys
import json
sys.path.append('../')
from my_app.app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.cntx = self.app.app_context()
        self.cntx.push()
        db.create_all()
        self.bucketlist = {'name': 'Vacation'}

        self.user_data = {
            'username': 'vicky',
            'email': 'v@gmail.com',
            'password': 'password'
        }
        self.user_login = {
            'username': 'vicky',
            'password': 'password'

        }
        self.client().post('/api/v1/auth/register', data=self.user_data)
        # self.client().post('/api/v1/auth/login', data=self.user_login)


    def tearDown(self):
        """reset all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_token(self):
        """Return authentication token."""
        response = self.client().post("/api/v1/auth/login",
                          data=self.user_login)
        output = json.loads(response.data.decode())
        token = output["access_token"]
        return {"access_token": token}

    def test_successful_bucketlist_creation(self):
        """
        Test that the API can create a bucketlist successfully
        using a POST request
        """
        response = self.client().post('/api/v1/bucketlists/', data=
            self.bucketlist, headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())
        self.assertIn('Vacation', str(output['name']))

    def test_create_bucketlist_with_name_not_string(self):
        """Test create a bucketlist with a name that is not a string."""
        response = self.client().post('/api/v1/bucketlists/', data=
            {"name": "#$%^&&&&^%$"}, headers=self.get_token())
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['name'][0], "Invalid characters")

    def test_create_bucketlist_without_name(self):
        """Test create a bucketlist without a name."""
        response = self.client().post('/api/v1/bucketlists/', data={
            'name': ' '}, headers=self.get_token())
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['name'][0], "Shorter than minimum length 3.")

    def test_create_bucketlist_that_already_exists(self):
        """Test create a bucketlist that already exists."""
        self.client().post('/api/v1/bucketlists/', data=
            self.bucketlist, headers=self.get_token())
        response = self.client().post('/api/v1/bucketlists/', data=
            self.bucketlist, headers=self.get_token())
        self.assertEqual(response.status_code, 409)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['message'], "The bucketlist already exists!")

    def test_api_can_get_all_bucketlists(self):
        """Test that the API can get all the bucketlists."""
        self.client().post('/api/v1/bucketlists/', data=
            self.bucketlist, headers=self.get_token())
        response = self.client().get('/api/v1/bucketlists/', headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertIn('Vacation', output[0]["name"])

    def test_api_getting_bucketlists_when_none_exists(self):
        """Test get busketlists when none exists."""
        response = self.client().get('/api/v1/bucketlists/', headers=self.get_token())
        self.assertEqual(response.status_code, 404)

    def test_api_can_get_bucketlist_by_id(self):
        """Test that the API can get a single bucketlist by id."""
        self.client().post('/api/v1/bucketlists/', data=
            self.bucketlist, headers=self.get_token())
        result = self.client().get(
            '/api/v1/bucketlists/1', headers=self.get_token())
        self.assertEqual(result.status_code, 200)
        output = json.loads(result.data.decode())
        self.assertIn('Vacation', output['name'])

    def test_bucketlist_can_be_updated(self):
        """Test that the API can update an existing bucketlist."""
        self.client().post('/api/v1/bucketlists/', data=
            {'name': 'Adventure'}, headers=self.get_token())
        response = self.client().put('/api/v1/bucketlists/1', data=
            {"name": "Go for adventure!"}, headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        result = self.client().get('/api/v1/bucketlists/1', headers=self.get_token())
        output = json.loads(result.data.decode())
        self.assertIn('Go for adventure', output['name'])

    def test_bucketlist_update_bucketlist_with_same_data(self):
        """Test that the API can update an existing bucketlist."""
        self.client().post('/api/v1/bucketlists/', data=
            {'name': 'Adventure'}, headers=self.get_token())
        response = self.client().put('/api/v1/bucketlists/1', data=
            {"name": "Adventure"}, headers=self.get_token())
        self.assertEqual(response.status_code, 409)

    def test_update_bucketlist_that_does_not_exist(self):
        """Test that the API can edit an existing bucketlist."""
        response = self.client().put('/api/v1/bucketlists/1', data=
            {"name": "Go for adventure!"}, headers=self.get_token())
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data.decode())
        self.assertIn('The bucketlist does not exist.', output['message'])

    def test_successful_bucketlist_deletion(self):
        """Test that the API can delete an existing bucketlist."""
        self.client().post('/api/v1/bucketlists/', data={
            'name': 'Go shopping'}, headers=self.get_token())
        response = self.client().delete('/api/v1/bucketlists/1', headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        result = self.client().get('/api/v1/bucketlists/1', headers=self.get_token())
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlist_that_does_not_exist(self):
        """Tests for the deletion of a bucketlist that does not exist."""
        response = self.client().delete('/api/v1/bucketlists/10', headers=self.get_token())
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
