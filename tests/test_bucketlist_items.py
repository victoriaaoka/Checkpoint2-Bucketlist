import unittest
import os
import sys
import json
sys.path.append('../')
from my_app.app import create_app, db


class BucketlistItemTestCase(unittest.TestCase):
    """This class represents the bucketlist-item test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        self.cntx = self.app.app_context()
        self.cntx.push()
        db.drop_all()
        db.create_all()
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
        self.client().post('/api/v1/auth/register', data=
            self.user_data)

    def tearDown(self):
        """reset all initialized variables."""
        db.session.remove()
        db.drop_all()
        self.cntx.pop()


    def get_token(self):
        """Return authentication token."""
        response = self.client().post("/api/v1/auth/login",
                          data=self.user_login)
        output = json.loads(response.data.decode())
        token = output["access_token"]
        return {"access_token": token}

    def test_create_a_bucketlist_item_successfully(self):
        """ Tests endpoint can create new bucketlist item."""
        self.client().post('/api/v1/bucketlists/',
            data = self.bucketlist, headers=self.get_token())
        response = self.client().post('/api/v1/bucketlists/1/items/', data=
             self.bucketlist_item, headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())
        self.assertIn('Tokyo', output['name'])

    def test_create_a_bucketlist_item_without_name(self):
        """ Tests endpoint can create new bucketlist item."""
        new_bucketlist_item = {'name': ' '}
        self.client().post('/api/v1/bucketlists/',
            data=self.bucketlist, headers=self.get_token())
        response = self.client().post('/api/v1/bucketlists/1/items/', data=
             new_bucketlist_item, headers=self.get_token())
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['name'][0], "Shorter than minimum length 3.")

    def test_create_a_bucketlist_item_that_exists(self):
        """ Tests the creation of a bucketlist item that already exists."""
        self.client().post('/api/v1/bucketlists/',
            data=self.bucketlist, headers=self.get_token())
        self.client().post('/api/v1/bucketlists/1/items/', data=
             self.bucketlist_item, headers=self.get_token())
        response = self.client().post('/api/v1/bucketlists/1/items/', data=
             self.bucketlist_item, headers=self.get_token())
        self.assertEqual(response.status_code, 409)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['message'], "The bucketlist item already exists!")

    def test_update_a_bucketlist_item(self):
        """Tests that a bucketlist item can be updated."""
        self.client().post('/api/v1/bucketlists/',
            data=self.bucketlist, headers=self.get_token())
        self.client().post('/api/v1/bucketlists/1/items/',
            data=self.bucketlist_item, headers=self.get_token())
        response = self.client().put('/api/v1/bucketlists/1/items/1', data={
            'name': 'Go to Mombasa!'}, headers=self.get_token())
        self.assertEqual(response.status_code, 200)

    def test_edit_a_bucketlist_item_that_does_not_exist(self):
        """Tests that a bucketlist item that does not exist can not be updated."""
        self.client().post('/api/v1/bucketlists/',
            data=self.bucketlist, headers=self.get_token())
        response = self.client().put('/api/v1/bucketlists/1/items/1', data={
            'name': 'Go to Mombasa!'}, headers=self.get_token())
        self.assertEqual(response.status_code, 404)

    def test_update_a_bucketlist_item_with_same_data(self):
        """Tests that a bucketlist item cannot be updated with the same data."""
        self.client().post('/api/v1/bucketlists/', data=self.bucketlist, headers=self.get_token())
        self.client().post('/api/v1/bucketlists/1/items/', data=
            self.bucketlist_item, headers=self.get_token())
        response = self.client().put('/api/v1/bucketlists/1/items/1', data={
            'name': 'Go to Tokyo'}, headers=self.get_token())
        self.assertEqual(response.status_code, 409)

    def test_successful_bucketlist_item_deletion(self):
        """Test that the API can delete an existing bucketlist."""
        self.client().post('/api/v1/bucketlists/', data={'name': 'Go shopping'},
            headers=self.get_token())
        self.client().post('/api/v1/bucketlists/1/items/',
            data=self.bucketlist_item, headers=self.get_token())
        response = self.client().delete('/api/v1/bucketlists/1/items/1',
            headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        result = self.client().delete('/api/v1/bucketlists/1/items/1',
            headers=self.get_token())
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlist_item_that_does_not_exist(self):
        """Test the deletion of a bucketlist item that does not exist."""
        self.client().post('/api/v1/bucketlists/', data={'name': 'Go shopping'},
            headers=self.get_token())
        resp = self.client().delete('/api/v1/bucketlists/1/items/2',
            headers=self.get_token())
        self.assertEqual(resp.status_code, 404)
