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

    def test_get_teams(self):
        result = [{"id": 1, "name": "FuRy", "description": "Andrew is a god"}, {"id": 2, "name": "Artemis", "description": "Not your average expieriance"}, {"id": 3, "name": "Faze", "description": "Olof is a criminal"}, {"id": 4, "name": "Outer Heavan", "description": "... wtf"}]
        r = requests.get(url + 'teams')
        self.assertEqual(result, r.json())

    def test_get_team(self):
        result = {"id": 1, "name": "FuRy", "description": "Andrew is a god"}
        r = requests.get(url + 'teams/1')
        self.assertEqual(result, r.json())

    def test_get_team_leagues(self):
        result = [{"id": 1, "name": "Ignis", "owner_id": 1, "entry_fee": 100, "description": "Best place to play!"}, {"id": 2, "name": "VGL", "owner_id": 2, "entry_fee": 1000, "description": "Second Best place to play!"}]
        r = requests.get(url + 'teams/1/leagues')
        self.assertEqual(result, r.json())

    def test_get_team_users(self):
        result = [{"id":1,"username":"Caleb","permission":2,"is_owner_team":1,"description":"Just your average player","role":1}, {"id":3,"username":"Gucci","permission":0,"is_owner_team":0,"description":"I like shaggy","role":2}]
        r = requests.get(url + 'teams/1/users')
        self.assertEqual(result, r.json())

    def test_post_team(self):
        r = requests.post(url + 'teams', data={"name": "Test", "description": "Test", "team_key": 'root', "user_id": 1}, headers={"request_key":"root"})
        self.assertEqual(200, r.status_code)

    def test_edit_team(self):
        result = {"id": 1, "name": "Test", "description": "Test"}
        r = requests.put(url + 'teams/1', data={"name": "Test", "description": "Test"}, headers={'request_key': 'root'})
        r2 = requests.get(url + 'teams/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_delete_team(self):
        r = requests.delete(url + 'teams/1', headers={'request_key':'root'})
        r2 = requests.get(url + 'teams/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()