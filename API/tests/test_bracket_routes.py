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

    def test_get_brackets(self):
        result = [{"id": 3, "tournament_id": 1, "team_id": 3, "place": 1, "games_won": 2, "games_tied": 0, "games_lost": 0, "games_played": 2, "score": None}, {"id": 2, "tournament_id": 1, "team_id": 2, "place": 2, "games_won": 1, "games_tied": 0, "games_lost": 1, "games_played": 2, "score": None}, {"id": 1, "tournament_id": 1, "team_id": 1, "place": 3, "games_won": 1, "games_tied": 0, "games_lost": 1, "games_played": 2, "score": None}, {"id": 4, "tournament_id": 1, "team_id": 4, "place": 4, "games_won": 0, "games_tied": 0, "games_lost": 2, "games_played": 2, "score": None}]
        r = requests.get(url + 'tournaments/1/brackets')
        self.assertEqual(result, r.json())

    def test_get_bracket(self):
        result = {"id": 3, "tournament_id": 1, "team_id": 3, "place": 1, "games_won": 2, "games_tied": 0, "games_lost": 0, "games_played": 2, "score": None}
        r = requests.get(url + 'tournaments/1/brackets/3')
        self.assertEqual(result, r.json())

    def test_post_bracket(self):
        r = requests.post(url + 'tournaments/2/brackets', data={"team_id": 3, "place": 1, "games_won": 0, "games_tied": 0, "games_lost": 0, "games_played": 0, "score": None})
        self.assertEqual(200, r.status_code)

    def test_edit_bracket(self):
        result = [{"id": 3, "tournament_id": 1, "team_id": 3, "place": 1, "games_won": 2, "games_tied": 0, "games_lost": 0, "games_played": 2, "score": None}, {"id": 2, "tournament_id": 1, "team_id": 2, "place": 2, "games_won": 1, "games_tied": 0, "games_lost": 1, "games_played": 2, "score": None}, {"id": 1, "tournament_id": 1, "team_id": 1, "place": 3, "games_won": 1, "games_tied": 0, "games_lost": 1, "games_played": 2, "score": None}, {"id": 4, "tournament_id": 1, "team_id": 4, "place": 4, "games_won": 0, "games_tied": 0, "games_lost": 2, "games_played": 2, "score": None}]
        r = requests.put(url + 'tournaments/1/brackets/1', data={"place": 2, "games_won": 2, "games_tied": 0, "games_lost": 1, "games_played": 3}, headers={'request_key':'root'})
        r2 = requests.get(url + 'tournaments/1/brackets')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_delete_bracket(self):
        r = requests.delete(url + 'tournaments/1/brackets/1', headers={'request_key':'root'})
        r2 = requests.get(url + 'tournaments/1/brackets/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)