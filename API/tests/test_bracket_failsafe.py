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

    def test_fail_get_brackets(self):
        cur.execute('DELETE FROM `brackets` WHERE 1=1;')
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'tournaments/1/brackets')
        self.assertEqual(404, r.status_code)

    def test_fail_get_brackets(self):
        cur.execute('DELETE FROM `brackets` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'tournaments/1/brackets/1')
        self.assertEqual(404, r.status_code)

    def test_fail_post_brackets(self):
        r = requests.post(url + 'tournaments/1/brackets', data={"team_id":7, "place": 1}, headers={'request_key': 'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_post_brackets(self):
        r = requests.post(url + 'tournaments/2/brackets', data={"team_id":2, "place": 1})
        self.assertEqual(409, r.status_code)

    def test_fail_edit_brackets(self):
        cur.execute('DELETE FROM `brackets` WHERE 1=1;')
        conn.commit()
        r = requests.put(url + 'tournaments/1/brackets/1', data={"place": 2, "games_won": 2, "games_tied": 0, "games_lost": 1, "games_played": 3}, headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_edit_league(self):
        r = requests.put(url + 'tournaments/1/brackets/1', data={"place": 2, "games_won": 2, "games_tied": 0, "games_lost": 1, "games_played": 3})
        self.assertEqual(409, r.status_code)

    def test_fail_delete_brackets(self):
        cur.execute('DELETE FROM `brackets` WHERE 1=1;')
        conn.commit()
        r = requests.delete(url + 'tournaments/1/brackets/1', headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_delete_league(self):
        r = requests.delete(url + 'tournaments/1/brackets/1')
        self.assertEqual(409, r.status_code)

if __name__ == '__main__':
    unittest.main()