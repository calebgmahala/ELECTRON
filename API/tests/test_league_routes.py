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

    def test_get_league_tournaments(self):
        result = [{"id": 1, "organizer_id": 1, "name": "New Year", "type": 2, "size": 8, "start_date": "2018-01-01 08:00:00", "end_date": "2018-01-20", "entry_fee": "1000.00", "description": "New year special"}, {"id": 2, "organizer_id": 1, "name": "Christmas", "type": 1, "size": 4, "start_date": "2018-12-25 12:30:00", "end_date": None, "entry_fee": "5.00", "description": "Christmas special"}]
        r = requests.get(url + 'leagues/1/tournaments')
        self.assertEqual(result, r.json())

    def test_get_league_teams(self):
        result = [{"id": 1, "name": "FuRy", "owner_id": 1, "description": "Andrew is a god"}, {"id": 2, "name": "Artemis", "owner_id": 2, "description": "Not your average expieriance"}, {"id": 3, "name": "Faze", "owner_id": 2, "description": "Olof is a criminal"}, {"id": 4, "name": "Outer Heavan", "owner_id": 1, "description": "... wtf"}]
        r = requests.get(url + 'leagues/1/teams')
        self.assertEqual(result, r.json())

    def test_get_league_teams_requests(self):
        result = [{"id": 2, "name": "Artemis", "owner_id": 2, "description": "Not your average expieriance"}]
        r = requests.get(url + 'leagues/2/teams/requests')
        self.assertEqual(result, r.json())

    def test_post_team_leagues(self):
        r = requests.get(url + 'leagues/1/teams', data={"organizer_id":2, "team_id":3})
        self.assertEqual(200, r.status_code)

    def test_post_league(self):
        r = requests.post(url + 'leagues', data={"name": "Test", "owner_id": 1, "entry_fee": 1000, "description": "Test"})
        self.assertEqual(200, r.status_code)

    def test_edit_league(self):
        result = {"id": 1, "name": "Test", "owner_id": 1, "entry_fee": "10.00", "description": "Test"}
        r = requests.put(url + 'leagues/1', data={"name": "Test", "owner_id": 1, "entry_fee": 1000, "description": "Test"})
        r2 = requests.get(url + 'leagues/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_edit_league_teams(self):
        r = requests.put(url + 'leagues/2/teams/2', data={"request": 0})
        r2 = requests.get(url + 'leagues/2/teams/requests')
        self.assertEqual(200, r.status_code)
        self.assertEqual([], r2.json())

    def test_delete_league(self):
        r = requests.delete(url + 'leagues/1')
        r2 = requests.get(url + 'leagues/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

    def test_delete_team_leagues(self):
        r = requests.delete(url + 'leagues/1/teams/1')
        r2 = requests.get(url + 'leagues/1/teams/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()