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

    def test_get_users(self):
        result = [{"id": 1, "username": "Caleb", "team_id": 1, "is_owner_team": 0, "description": "Just your average player", "role": 1}, {"id": 2, "username": "Bobby", "team_id": 3, "is_owner_team": 0, "description": "pass me another cold one", "role": 1}, {"id": 3, "username": "Gucci", "team_id": 1, "is_owner_team": 0, "description": "I like shaggy", "role": 2}]
        r = requests.get(url + 'users')
        self.assertEqual(result, r.json())

    def test_get_user(self):
        result = {"id": 1, "username": "Caleb", "team_id": 1, "is_owner_team": 0, "description": "Just your average player", "role": 1}
        r = requests.get(url + 'users/1')
        self.assertEqual(result, r.json())

    def test_post_user(self):
        r = requests.post(url + 'users', data={'username': 'Test', 'password': 'root'})
        r2 = requests.post(url + 'login', data={'username': 'Test', 'password': 'root'})
        self.assertEqual(200, r.status_code)
        self.assertEqual(200, r2.status_code)

    def test_login_user(self):
        r = requests.post(url + 'login', data={'username': 'Caleb', 'password': 'root'})
        self.assertEqual(200, r.status_code)

    def test_delete_user(self):
        r = requests.delete(url + 'users/1')
        r2 = requests.get(url + 'users/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()