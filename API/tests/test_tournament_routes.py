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

    def test_get_tournaments(self):
        result = [{"id": 1, "organizer_id": 1, "name": "New Year", "type": 2, "size": 8, "start_date": "2018-01-01 08:00:00", "end_date": "2018-01-20", "entry_fee": "1000.00", "description": "New year special"}, {"id": 2, "organizer_id": 1, "name": "Christmas", "type": 1, "size": 4, "start_date": "2018-12-25 12:30:00", "end_date": None, "entry_fee": "5.00", "description": "Christmas special"}]
        r = requests.get(url + 'tournaments')
        self.assertEqual(result, r.json())

    def test_get_tournament(self):
        result = {"id": 1, "organizer_id": 1, "name": "New Year", "type": 2, "size": 8, "start_date": "2018-01-01 08:00:00", "end_date": "2018-01-20", "entry_fee": "1000.00", "description": "New year special"}
        r = requests.get(url + 'tournaments/1')
        self.assertEqual(result, r.json())

    def test_post_tournament(self):
        r = requests.post(url + 'tournaments', data={"name": "Test", "type": 1, "organizer_id": 1, "size": 4, "start_date": "2018-12-30 20:00:00", "entry_fee": 1000, "description": "Test"}, headers={'request_key':'root'})
        self.assertEqual(200, r.status_code)

    def test_edit_tournament(self):
        result = {"id": 1, "organizer_id": 1, "name": "Test", "type": 2, "size": 2, "start_date": "2018-01-02 08:00:00", "end_date": "2018-01-23", "entry_fee": "100.00", "description": "Test"}
        r = requests.put(url + 'tournaments/1', data={"name": "Test", "type": 2, "organizer_id": 1, "size": 2, "start_date": "2018-01-02 08:00:00", "end_date": "2018-01-23", "entry_fee": 10000, "description": "Test"}, headers={'request_key':'root'})
        r2 = requests.get(url + 'tournaments/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(result, r2.json())

    def test_delete_tournament(self):
        r = requests.delete(url + 'tournaments/1', headers={'request_key':'root'})
        r2 = requests.get(url + 'tournaments/1')
        self.assertEqual(200, r.status_code)
        self.assertEqual(404, r2.status_code)

if __name__ == '__main__':
    unittest.main()