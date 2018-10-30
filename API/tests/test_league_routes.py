import unittest
import os
import requests
import mysql.connector

url = "http://localhost:5000/"

conn = mysql.connector.connect(user='root', database='test')
cur = conn.cursor()

def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        if command.strip() != '':
            cur.execute(command)

class Requests(unittest.TestCase):

    def setUp(self):
        executeScriptsFromFile('test.sql')
        conn.commit()

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
        self.assertEqual(200, r.status_code)

    def test_edit_league(self):
        result = {"id": 1, "name": "Test", "owner_id": 1, "entry_fee": "10.00", "description": "Test"}
        r = requests.put(url + 'leagues/1', data={"name": "Test", "owner_id": 1, "entry_fee": 1000, "description": "Test"})
        r2 = requests.get(url + 'leagues/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_delete_league(self):
        r = requests.delete(url + 'leagues/1')
        r2 = requests.get(url + 'leagues/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()