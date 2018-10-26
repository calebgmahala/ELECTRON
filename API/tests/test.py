import unittest
import os
import requests
from api import app

url = "http://localhost:5000/"

@classmethod
def tearDown(Requests):
    app.env = 'production'

class Requests(unittest.TestCase):

    def setUp(self):
        app.env = 'test'

    def test_db_connection(self):
        self.assertEqual(app.env, 'test')

    def test_get_leagues(self):
        result = [{"id": 1, "name": "Ignis", "owner_id": 1, "entry_fee": "1.00", "description": "Best place to play!"}, {"id": 2, "name": "VGL", "owner_id": 2, "entry_fee": "10.00", "description": "Second Best place to play!"}]
        r = requests.get(url + 'leagues')
        self.assertEqual(result, r.json())

    def test_get_league(self):
        result = {"id": 1, "name": "Ignis", "owner_id": 1, "entry_fee": "1.00", "description": "Best place to play!"}
        r = requests.get(url + 'leagues/1')
        self.assertEqual(result, r.json())

    def test_post_league(self):
        r = requests.post(url + 'leagues', data={"name": "Test", "owner_id": 1, "entry_fee": 1000, "description": "Test"})

if __name__ == '__main__':
    unittest.main()