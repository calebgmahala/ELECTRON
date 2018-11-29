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

class FailRequests(unittest.TestCase):

    def setUp(self):
        executeScriptsFromFile('test.sql')
        conn.commit()

    def test_fail_get_league(self):
        cur.execute('DELETE FROM brackets WHERE 1=1')
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'leagues/1')
        self.assertEqual(404, r.status_code)

    def test_fail_get_league_tournaments(self):
        cur.execute('DELETE FROM brackets WHERE 1=1')
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'leagues/4/tournaments')
        self.assertEqual(404, r.status_code)

    def test_fail_get_league_teams(self):
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'leagues/4/teams')
        self.assertEqual(404, r.status_code)

    def test_fail_post_team_leagues(self):
        r = requests.post(url + 'leagues/1/teams', data={"organizer_id":7, "team_id":1 }, headers={'request_key': 'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_post_team_leagues(self):
        r = requests.post(url + 'leagues/1/teams', data={"organizer_id":1, "team_id":1})
        self.assertEqual(409, r.status_code)

    def test_fail_post_league(self):
        r = requests.post(url + 'leagues', data={"owner_id": 1, "description": "Test"}, headers={'request_key': 'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_post_league(self):
        r = requests.post(url + 'leagues', data={"name": "Test", "owner_id": 1, "organizer_key": "test", "description": "Test"})
        self.assertEqual(409, r.status_code)

    def test_fail_edit_league(self):
        cur.execute('DELETE FROM brackets WHERE 1=1')
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers` WHERE 1=1;')
        conn.commit()
        r = requests.put(url + 'leagues/1', data={"owner_id": 1, "description": "Test"}, headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_edit_league(self):
        r = requests.put(url + 'leagues/1', data={"owner_id": 1, "description": "Test"})
        self.assertEqual(409, r.status_code)

    def test_fail_edit_league_teams(self):
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        conn.commit()
        r = requests.put(url + 'leagues/2/teams/2', data={"request": 0}, headers={'request_key': 'root2'})
        self.assertEqual(404, r.status_code)

    def test_fail_delete_league(self):
        cur.execute('DELETE FROM brackets WHERE 1=1')
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers` WHERE 1=1;')
        conn.commit()
        r = requests.delete(url + 'leagues/1', headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_delete_league(self):
        r = requests.delete(url + 'leagues/1')
        self.assertEqual(409, r.status_code)

    def test_fail_delete_team_leagues(self):
        r = requests.delete(url + 'leagues/1/teams/7', headers={'request_key': 'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_delete_team_leagues(self):
        r = requests.delete(url + 'leagues/2/teams/2')
        self.assertEqual(409, r.status_code)

if __name__ == '__main__':
    unittest.main()