import unittest
import os
import sys
import json
sys.path.append('../')
from my_app import create_app, db


class BucketlistItemTestCase(unittest.TestCase):
    """This class represents the bucketlist-item test case"""

    def setUp(self):
        """Define test variables and initialize app."""
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
        self.client().post('v1/auth/register', data=json.dumps(
            self.user_data))
        self.client().post('v1/auth/login', data=json.dumps(
            self.user_login))

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """reset all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_a_bucketlist_item_successfully(self):
        """ Tests endpoint can create new bucketlist item."""
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        response = self.client().post('/bucketlists/1/items/', data=json.dumps(
             self.bucketlist_item))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Tokyo', str(response.data))

    def test_create_a_bucketlist_item_without_name(self):
        """ Tests endpoint can create new bucketlist item."""
        new_bucketlist_item = {'name': ' '}
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        response = self.client().post('/bucketlists/1/items/', data=json.dumps(
             new_bucketlist_item))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response['message'], "The bucketlist item name should be entered! ")

    def test_create_a_bucketlist_item_that_exists(self):
        """ Tests the creation of a bucketlist item that already exists."""
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        self.client().post('/bucketlists/1/items/', data=json.dumps(
             self.bucketlist_item))
        response = self.client().post('/bucketlists/1/items/', data=json.dumps(
             self.bucketlist_item))
        self.assertEqual(response.status_code, 409)
        self.assertEqual(
            response['message'], "The bucketlist item already exists! ")

    def test_api_can_get_all_bucketlist_items(self):
        """Test that the API can get all the bucketlist items."""
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        self.client().post('/bucketlists/1/items/', data=json.dumps(
            self.bucketlist_item))
        response = self.client().get('/bucketlists/1/items/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Tokyo', str(response.data))

    def test_retrieving_bucketlist_items_when_none_exists(self):
        """Test retrieving bucketlist items when none exists."""
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        response = self.client().get('/bucketlists/1/items/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response['message'], "There are no bucketlist items created yet.")

    def test_update_a_bucketlist_item(self):
        """Tests that a bucketlist item can be updated."""
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        self.client().post('/bucketlists/1/items/', data=json.dumps(
            self.bucketlist_item))
        response = self.client().put('/bucketlists/1/items/1', data={
            'name': 'Go to Mombasa!'})
        self.assertEqual(response.status_code, 200)
        result = self.client().get('/bucketlists/1/items/1')
        self.assertIn('Mombasa', str(result.data))

    def test_edit_a_bucketlist_item_that_does_not_exist(self):
        """Tests that a bucketlist item that does not exist can not be updated."""
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        response = self.client().put('/bucketlists/1/items/1', data={
            'name': 'Go to Mombasa!'})
        self.assertEqual(response.status_code, 400)

    def test_update_a_bucketlist_item_with_same_data(self):
        """Tests that a bucketlist item cannot be updated with the same data."""
        self.client().post('/bucketlists/', data=json.dumps(self.bucketlist))
        self.client().post('/bucketlists/1/items/', data=json.dumps(
            self.bucketlist_item))
        response = self.client().put('/bucketlists/1/items/1', data={
            'name': 'Go to Tokyo'})
        self.assertEqual(response.status_code, 409)

    def test_successful_bucketlist_item_deletion(self):
        """Test that the API can delete an existing bucketlist."""
        self.client().post('/bucketlists/', data={'name': 'Go shopping'})
        self.client().post('/bucketlists/1/items/', data=json.dumps(
            self.bucketlist_item))
        response = self.client().delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 200)
        result = self.client().get('/bucketlists/1/items/1')
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlist_item_that_does_not_exist(self):
        """Test the deletion of a bucketlist item that does not exist."""
        resp = self.client().delete('/bucketlists/1/items/100')
        self.assertEqual(resp.status_code, 404)
