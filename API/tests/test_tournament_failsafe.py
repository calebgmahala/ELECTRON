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

    def test_fail_get_tournament(self):
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'tournaments/1')
        self.assertEqual(404, r.status_code)

    def test_fail_post_tournament(self):
        r = requests.post(url + 'tournaments', data={"name": 1, "description": "Test"})
        self.assertEqual(404, r.status_code)

    def test_fail_edit_tournament(self):
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        conn.commit()
        r = requests.put(url + 'tournaments/1', data={"name": 1, "description": "Test"})
        self.assertEqual(404, r.status_code)

    def test_fail_delete_tournament(self):
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        conn.commit()
        r = requests.delete(url + 'tournaments/1')
        self.assertEqual(404, r.status_code)

if __name__ == '__main__':
    unittest.main()