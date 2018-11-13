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

    def test_fail_get_user(self):
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers` WHERE 1=1;')
        cur.execute('DELETE FROM `users` WHERE 1=1;')
        conn.commit()
        r = requests.get(url + 'users/1')
        self.assertEqual(404, r.status_code)

    def test_fail_post_user(self):
        r = requests.post(url + 'users', data={'username': 'Test'})
        self.assertEqual(404, r.status_code)

    def test_fail_login_user(self):
        r = requests.post(url + 'login', data={'username': 'Caleb', 'password': 'fail'})
        self.assertEqual(404, r.status_code)

    def test_fail_delete_user(self):
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers` WHERE 1=1;')
        cur.execute('DELETE FROM `users` WHERE 1=1;')
        conn.commit()
        r = requests.delete(url + 'users/1')
        self.assertEqual(404, r.status_code)

if __name__ == '__main__':
    unittest.main()