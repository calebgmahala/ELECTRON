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

    def test_get_matches(self):
        result = [{"id": 1, "tournament_id": 1, "home_id": 3, "away_id": 1, "home_score": 16, "away_score": 10, "start_date": "2018-01-01 08:00:00", "end_date": "2018-01-01 09:00:00"}, {"id": 2, "tournament_id": 1, "home_id": 4, "away_id": 3, "home_score": 4, "away_score": 16, "start_date": "2018-03-01 08:00:00", "end_date": "2018-03-01 09:00:00"}, {"id": 3, "tournament_id": 1, "home_id": 2, "away_id": 1, "home_score": 15, "away_score": 16, "start_date": "2018-05-01 08:00:00", "end_date": "2018-05-01 09:00:00"}, {"id": 4, "tournament_id": 1, "home_id": 2, "away_id": 4, "home_score": 16, "away_score": 2, "start_date": "2018-08-01 10:00:00", "end_date": "2018-08-01 11:00:00"}]
        r = requests.get(url + 'tournaments/1/matches')
        self.assertEqual(result, r.json())

    def test_get_match(self):
        result = {"id": 1, "tournament_id": 1, "home_id": 3, "away_id": 1, "home_score": 16, "away_score": 10, "start_date": "2018-01-01 08:00:00", "end_date": "2018-01-01 09:00:00"}
        r = requests.get(url + 'matches/1')
        self.assertEqual(result, r.json())

    def test_post_match(self):
        r = requests.post(url + 'tournaments/1/matches', data={"home_id": 3, "away_id": 2, "start_date": "2018-1-01 20:00:00"}, headers={'organizer_key':'root'})
        self.assertEqual(200, r.status_code)

    def test_edit_match(self):
        result = {"id": 1, "tournament_id": 1, "home_id": 3, "away_id": 1, "home_score": 16, "away_score": 8, "start_date": "2018-01-01 08:00:00", "end_date": "2018-01-01 09:00:00"}
        r = requests.put(url + 'matches/1', data={"away_score": 8}, headers={'request_key':'root'})
        r2 = requests.get(url + 'matches/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_delete_match(self):
        r = requests.delete(url + 'matches/1', headers={'request_key':'root'})
        r2 = requests.get(url + 'matches/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()