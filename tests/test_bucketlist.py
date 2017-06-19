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
        with self.app.app_context():
            db.create_all()

    def test_bucketlist_creation(self):
        """
        Test that the API can create a bucketlist successfully
        using a POST request
        """
        res = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Vacation', str(res.data))

    def test_api_can_get_all_bucketlists(self):
        """Test that the API can get all the bucketlists."""
        resp = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        res = self.client().get('/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Vacation', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test that the API can get a single bucketlist by id."""
        resp = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Vacation', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test that the API can edit an existing bucketlist."""
        resp = self.client().post(
            '/bucketlists/',
            data={'name': 'Adventure'})
        self.assertEqual(resp.status_code, 201)
        res = self.client().put(
            '/bucketlists/1',
            data={
                "name": "Go for adventure!"
            })
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/bucketlists/1')
        self.assertIn('Go for adventure', str(result.data))

    def test_bucketlist_deletion(self):
        """Test that the API can delete an existing bucketlist."""
        resp = self.client().post(
            '/bucketlists/',
            data={'name': 'Go shopping'})
        self.assertEqual(resp.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """reset all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
