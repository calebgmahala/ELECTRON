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

    def test_get_match_leaderboards(self):
        result = [{"id": 2, "player_id": 3, "team_id": 1, "match_id": 1, "score": 20, "kills": 20, "assists": 0, "deaths": 5, "dpr": 170}, {"id": 1, "player_id": 1, "team_id": 1, "match_id": 1, "score": 10, "kills": 10, "assists": 2, "deaths": 8, "dpr": 76}, {"id": 3, "player_id": 2, "team_id": 3, "match_id": 1, "score": 13, "kills": 15, "assists": 4, "deaths": 7, "dpr": 82}]
        r = requests.get(url + 'matches/1/leaderboard')
        self.assertEqual(result, r.json())

    def test_get_match_leaderboard(self):
        result = {"id": 1, "player_id": 1, "team_id": 1, "match_id": 1, "score": 10, "kills": 10, "assists": 2, "deaths": 8, "dpr": 76}
        r = requests.get(url + 'matches/1/leaderboard/1')
        self.assertEqual(result, r.json())

    def test_post_match_leaderboard(self):
        r = requests.post(url + 'matches/1/leaderboard', data={"player_id":1, "team_id": 1, "match_id": 3}, headers={'organizer_key':'root'})
        self.assertEqual(200, r.status_code)

    def test_edit_match_leaderboard(self):
        result = {"id": 1, "player_id": 1, "team_id": 1, "match_id": 1, "score": 11, "kills": 10, "assists": 2, "deaths": 8, "dpr": 76}
        r = requests.put(url + 'matches/1/leaderboard/1', data={"score": 11}, headers={'request_key':'root'})
        r2 = requests.get(url + 'matches/1/leaderboard/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_delete_match_leaderboard(self):
        r = requests.delete(url + 'matches/1/leaderboard/1', headers={'request_key':'root'})
        r2 = requests.get(url + 'matches/1/leaderboard/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()