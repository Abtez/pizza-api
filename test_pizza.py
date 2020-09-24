import unittest
import os
import json
from app import create_app, db


class PizzaTestCase(unittest.TestCase):
    """This class represents the pizza test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.pizzas = {'name': 'Periperi'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_pizza_creation(self):
        """Test API can create a pizza (POST request)"""
        res = self.client().post('/pizzas/', data=self.pizzas)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Periperi', str(res.data))

    def test_api_can_get_all_pizzas(self):
        """Test API can get a pizza (GET request)."""
        res = self.client().post('/pizzas/', data=self.pizzas)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/pizzas/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Periperi', str(res.data))

    def test_api_can_get_pizzas_by_id(self):
        """Test API can get a single pizza by using it's id."""
        rv = self.client().post('/pizzas/', data=self.pizzas)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/pizzas/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Periperi', str(result.data))

    def test_pizza_deletion(self):
        """Test API can delete an existing pizza. (DELETE request)."""
        rv = self.client().post('/pizzas/',data={'name': 'periperi'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/pizzas/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/pizzas/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()