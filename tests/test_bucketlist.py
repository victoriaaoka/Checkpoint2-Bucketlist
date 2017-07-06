import unittest
import os
import sys
import json
sys.path.append('../')
from my_app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
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
        self.client().post('/auth/register', data=json.dumps(
            self.user_data))
        self.client().post('/auth/login', data=json.dumps(
            self.user_login))

        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        """reset all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_successful_bucketlist_creation(self):
        """
        Test that the API can create a bucketlist successfully
        using a POST request
        """
        response = self.client().post('/bucketlists/', data=json.dumps(
            self.bucketlist))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Vacation', str(response.data))

    def test_create_bucketlist_with_name_not_string(self):
        """Test create a bucketlist with a name that is not a string."""
        response = self.client().post('/bucketlists/', data=json.dumps(
            {"name": "5667899"}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response["message"], "Bucketlist name can only be of type string.")

    def test_create_bucketlist_without_name(self):
        """Test create a bucketlist without a name."""
        response = self.client().post('/bucketlists/', data=json.dumps({
            'name': ' '}))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response['message'], "Bucketlist name should be provided.")

    def test_create_bucketlist_that_already_exists(self):
        """Test create a bucketlist that already exists."""
        self.client().post('v1/bucketlists/', data=json.dumps(self.bucketlist))
        response = self.client().post('v1/bucketlists/', data=json.dumps(
            self.bucketlist))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response['message'], "The bucketlist already exists!")

    def test_api_can_get_all_bucketlists(self):
        """Test that the API can get all the bucketlists."""
        self.client().post('v1/bucketlists/', data=json.dumps(self.bucketlist))
        response = self.client().get('v1/bucketlists/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Vacation', str(response.data))

    def test_api_getting_bucketlists_when_none_exists(self):
        """Test get busketlists when none exists."""
        response = self.client().get('v1/bucketlists/')
        self.assertEqual(response.status_code, 404)

    def test_api_can_get_bucketlist_by_id(self):
        """Test that the API can get a single bucketlist by id."""
        self.client().post('v1/bucketlists/', data=json.dumps(
            self.bucketlist))
        result = self.client().get(
            'v1/bucketlists/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Vacation', str(result.data))

    def test_bucketlist_can_be_updated(self):
        """Test that the API can update an existing bucketlist."""
        self.client().post('v1/bucketlists/', data=json.dumps(
            {'name': 'Adventure'}))
        response = self.client().put('v1/bucketlists/1', data=json.dumps(
            {"name": "Go for adventure!"}))
        self.assertEqual(response.status_code, 200)
        result = self.client().get('v1/bucketlists/1')
        self.assertIn('Go for adventure', str(result.data))

    def test_update_bucketlist_that_does_not_exist(self):
        """Test that the API can edit an existing bucketlist."""
        self.client().post('v1/bucketlists/', data=json.dumps(
            {'name': 'Adventure'}))
        response = self.client().put('v1/bucketlists/1', data=json.dumps(
            {"name": "Go for adventure!"}))
        self.assertEqual(response.status_code, 200)
        result = self.client().get('v1/bucketlists/1')
        self.assertIn('Go for adventure', str(result.data))

    def test_successful_bucketlist_deletion(self):
        """Test that the API can delete an existing bucketlist."""
        self.client().post('v1/bucketlists/', data=json.dumps({
            'name': 'Go shopping'}))
        response = self.client().delete('v1/bucketlists/1')
        self.assertEqual(response.status_code, 200)
        result = self.client().get('v1/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlist_that_does_not_exist(self):
        """Tests for the deletion of a bucketlist that does not exist."""
        response = self.client().delete('v1/bucketlists/10')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
