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

    def test_fail_get_match(self):
        cur.execute('DELETE FROM `match_leaderboards` WHERE 1=1;')
        cur.execute('DELETE FROM `matches` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'matches/1')
        self.assertEqual(404, r.status_code)

    def test_fail_post_match(self):
        r = requests.post(url + 'tournaments/1/matches', data={"test": 3}, headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_post_match(self):
        r = requests.post(url + 'tournaments/1/matches', data={"home_id": 3, "away_id": 2, "start_date": "2018-1- 20:00:00"})
        self.assertEqual(409, r.status_code)

    def test_fail_edit_match(self):
        cur.execute('DELETE FROM `match_leaderboards` WHERE 1=1;')
        cur.execute('DELETE FROM `matches` WHERE 1=1;')
        conn.commit()
        r = requests.put(url + 'matches/1', data={"away_score": 16}, headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_edit_match(self):
        r = requests.put(url + 'matches/1', data={"away_score": 16})
        self.assertEqual(409, r.status_code)

    def test_fail_delete_match(self):
        cur.execute('DELETE FROM `match_leaderboards` WHERE 1=1;')
        cur.execute('DELETE FROM `matches` WHERE 1=1;')
        conn.commit()
        r = requests.delete(url + 'matches/1', headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_delete_match(self):
        r = requests.delete(url + 'matches/1')
        self.assertEqual(409, r.status_code)

if __name__ == '__main__':
    unittest.main()