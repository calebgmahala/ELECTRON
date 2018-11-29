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
        cur.execute('DELETE FROM brackets WHERE 1=1')
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

    def test_fail_put_user(self):
        cur.execute('DELETE FROM brackets WHERE 1=1')
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers` WHERE 1=1;')
        cur.execute('DELETE FROM `users` WHERE 1=1;')
        conn.commit()
        r = requests.put(url + 'users/1', data={'username': 'Test', 'description': 'test', 'role':0}, headers={'request_key':'test'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_put_user(self):
        r = requests.put(url + 'users/1', data={'username': 'Test', 'description': 'test', 'role':0}, headers={'request_key':'test'})
        self.assertEqual(409, r.status_code)
        r2 = requests.put(url + 'users/1', headers={'request_key':'root', 'team_id': '1', 'team_key': 'test'})
        self.assertEqual(409, r2.status_code)
        r3 = requests.put(url + 'users/1', headers={'request_key':'root', 'team_key': 'test'})
        self.assertEqual(409, r3.status_code)

    def test_fail_login_user(self):
        r = requests.post(url + 'login', data={'username': 'Caleb', 'password': 'fail'})
        self.assertEqual(404, r.status_code)

    def test_fail_logout_user(self):
        r = requests.delete(url + 'login', data={'id':1}, headers={'request_key':'root'})
        self.assertEqual(404, r.status_code)

    def test_fail_auth_logout_user(self):
        r = requests.delete(url + 'login', data={'id':1},)
        self.assertEqual(409, r.status_code)

    def test_fail_delete_user(self):
        cur.execute('DELETE FROM brackets WHERE 1=1')
        cur.execute('DELETE FROM `tournaments` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers_teams` WHERE 1=1;')
        cur.execute('DELETE FROM `organizers` WHERE 1=1;')
        cur.execute('DELETE FROM `users` WHERE 1=1;')
        conn.commit()
        r = requests.delete(url + 'users/1')
        self.assertEqual(404, r.status_code)

    def test_fail_auth_delete_user(self):
        r = requests.delete(url + 'users/1', headers={'request_key':'test'})
        self.assertEqual(409, r.status_code)

if __name__ == '__main__':
    unittest.main()