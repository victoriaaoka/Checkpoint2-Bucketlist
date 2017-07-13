import unittest
import os
import sys
sys.path.append('../')
from tests.base import BaseTestCase


class BucketlistTestCase(BaseTestCase):
    """This class represents the bucketlist test case"""

    def test_successful_bucketlist_creation(self):
        """
        Test that the API can create a bucketlist successfully
        using a POST request
        """
        response = self.client().post(
            '/api/v1/bucketlists/', data=self.bucketlist,
            headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode())
        self.assertIn('Vacation', str(output['name']))

    def test_create_bucketlist_with_name_not_string(self):
        """Test create a bucketlist with a name that is not a string."""
        response = self.client().post('/api/v1/bucketlists/', data={
            "name": "#$%^&&&&^%$"}, headers=self.get_token())
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['name'][0], 'Invalid characters')

    def test_create_bucketlist_without_name(self):
        """Test create a bucketlist without a name."""
        response = self.client().post('/api/v1/bucketlists/', data={
            'name': ' '}, headers=self.get_token())
        self.assertEqual(response.status_code, 400)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['name'][0], 'Shorter than minimum length 3.')

    def test_create_bucketlist_that_already_exists(self):
        """Test create a bucketlist that already exists."""
        self.client().post(
            '/api/v1/bucketlists/', data=self.bucketlist,
            headers=self.get_token())
        response = self.client().post(
            '/api/v1/bucketlists/', data=self.bucketlist,
            headers=self.get_token())
        self.assertEqual(response.status_code, 409)
        output = json.loads(response.data.decode())
        self.assertEqual(
            output['message'], 'The bucketlist already exists!')

    def test_api_can_get_all_bucketlists(self):
        """Test that the API can get all the bucketlists."""
        self.client().post(
            '/api/v1/bucketlists/', data=self.bucketlist,
            headers=self.get_token())
        response = self.client().get(
            '/api/v1/bucketlists/', headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode())
        self.assertIn('Vacation', output[0]['name'])

    def test_api_getting_bucketlists_when_none_exists(self):
        """Test get busketlists when none exists."""
        response = self.client().get(
            '/api/v1/bucketlists/', headers=self.get_token())
        self.assertEqual(response.status_code, 404)

    def test_api_can_get_bucketlist_by_id(self):
        """Test that the API can get a single bucketlist by id."""
        self.client().post(
            '/api/v1/bucketlists/', data=self.bucketlist,
            headers=self.get_token())
        result = self.client().get(
            '/api/v1/bucketlists/1', headers=self.get_token())
        self.assertEqual(result.status_code, 200)
        output = json.loads(result.data.decode())
        self.assertIn('Vacation', output['name'])

    def test_bucketlist_can_be_updated(self):
        """Test that the API can update an existing bucketlist."""
        self.client().post(
            '/api/v1/bucketlists/', data={'name': 'Adventure'},
            headers=self.get_token())
        response = self.client().put(
            '/api/v1/bucketlists/1', data={'name': 'Go for adventure!'},
            headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        result = self.client().get(
            '/api/v1/bucketlists/1',
            headers=self.get_token())
        output = json.loads(result.data.decode())
        self.assertIn('Go for adventure', output['name'])

    def test_bucketlist_update_bucketlist_with_same_data(self):
        """Test that the API can update an existing bucketlist."""
        self.client().post(
            '/api/v1/bucketlists/', data={'name': 'Adventure'},
            headers=self.get_token())
        response = self.client().put(
            '/api/v1/bucketlists/1', data={'name': 'Adventure'},
            headers=self.get_token())
        self.assertEqual(response.status_code, 409)

    def test_update_bucketlist_that_does_not_exist(self):
        """Test that the API can edit an existing bucketlist."""
        response = self.client().put(
            '/api/v1/bucketlists/1', data={'name': 'Go for adventure!'},
            headers=self.get_token())
        self.assertEqual(response.status_code, 404)
        output = json.loads(response.data.decode())
        self.assertIn('The bucketlist does not exist.', output['message'])

    def test_successful_bucketlist_deletion(self):
        """Test that the API can delete an existing bucketlist."""
        self.client().post('/api/v1/bucketlists/', data={
            'name': 'Go shopping'}, headers=self.get_token())
        response = self.client().delete(
            '/api/v1/bucketlists/1',
            headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        result = self.client().get(
            '/api/v1/bucketlists/1',
            headers=self.get_token())
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlist_that_does_not_exist(self):
        """Tests for the deletion of a bucketlist that does not exist."""
        response = self.client().delete(
            '/api/v1/bucketlists/10',
            headers=self.get_token())
        self.assertEqual(response.status_code, 404)

    def test_search_bucketlists_by_name(self):
        """Tests for searching a bucketlist by name."""
        self.client().post('/api/v1/bucketlists/', data={
            'name': 'Go shopping'}, headers=self.get_token())
        response = self.client().get(
            '/api/v1/bucketlists/?q=shop',
            headers=self.get_token())
        output = json.loads(response.data.decode())
        self.assertIn('shop', output[0]['name'])
        self.assertEqual(response.status_code, 200)

    def test_bucketlist_creation_without_token(self):
        """
        Test that a user cannot create a bucketlist without a token
        """
        response = self.client().post(
            '/api/v1/bucketlists/', data=self.bucketlist)
        self.assertEqual(response.status_code, 401)

    def test_bucketlist_pagination(self):
        """
        Test the use of pagination in getting bucketlists.
        """
        response = self.client().post(
            '/api/v1/bucketlists/',
            data=self.bucketlist, headers=self.get_token())
        response = self.client().post('/api/v1/bucketlists/', data={
            'name': 'Go shopping'}, headers=self.get_token())
        response = self.client().get(
            '/api/v1/bucketlists/?limit=1',
            headers=self.get_token())
        output = json.loads(response.data.decode())
        self.assertEqual(1, len(output))


if __name__ == '__main__':
    unittest.main()
