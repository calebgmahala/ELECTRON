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
        result = [{"id": 1, "name": "FuRy", "owner_id": 1, "description": "Andrew is a god"}, {"id": 2, "name": "Artemis", "owner_id": 2, "description": "Not your average expieriance"}, {"id": 3, "name": "Faze", "owner_id": 2, "description": "Olof is a criminal"}, {"id": 4, "name": "Outer Heavan", "owner_id": 1, "description": "... wtf"}]
        r = requests.get(url + 'teams')
        self.assertEqual(result, r.json())

    def test_get_team(self):
        result = {"id": 1, "name": "FuRy", "owner_id": 1, "description": "Andrew is a god"}
        r = requests.get(url + 'teams/1')
        self.assertEqual(result, r.json())

    def test_post_team(self):
        r = requests.post(url + 'teams', data={"name": "Test", "owner_id": 1, "description": "Test"})
        self.assertEqual(200, r.status_code)

    def test_edit_team(self):
        result = {"id": 1, "name": "Test", "owner_id": 1, "description": "Test"}
        r = requests.put(url + 'teams/1', data={"name": "Test", "owner_id": 1, "description": "Test"})
        r2 = requests.get(url + 'teams/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_delete_team(self):
        r = requests.delete(url + 'teams/1')
        r2 = requests.get(url + 'teams/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()