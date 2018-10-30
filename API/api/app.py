from flask import Flask, make_response, request, redirect, Response
# using flask as api framework
import mysql.connector
#used to pull mysql database
from flask_cors import CORS, cross_origin
#used to allow requests
import simplejson as json
#used to decode and encode json
import os

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
cors = CORS(app)
env = 'test'

#connect to mysql database
def connect_db():
	return mysql.connector.connect(user='root', database=env, host='localhost')


#set connection and cursor variables\
conn = connect_db()
cur = conn.cursor()

#league routes
@app.route("/leagues", methods=['GET', 'POST'])
def leagues():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all organizers
		resp = []
		cur.execute("SELECT * FROM organizers")
		org = cur.fetchall()
		for a in range(len(org)):
			money = str(org[a][3])[:-2] + "." + str(org[a][3])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			resp.append({"id":org[a][0], "name":org[a][1], "owner_id":org[a][2], "entry_fee":money, "description":org[a][4]}) # change entry fee value to the string (had to make a new array because you can't change tuple values)
		return json.dumps(resp)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		try: 
			body['entry_fee'] = int(body['entry_fee'])
			cur.execute('INSERT INTO organizers (name, entry_fee, owner_id, description) VALUES(%(name)s, %(entry_fee)s, 1, %(description)s)', body)
			conn.commit()
			return Response(status=200)
		except (mysql.connector.Error, KeyError) as err:
			print(err)
			return Response(status=404)

@app.route("/leagues/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def showleague(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		org = cur.fetchone()
		resp = ''
		if (org is None):
			resp = Response(status=404)
			return resp
		else:
			money = str(org[3])[:-2] + "." + str(org[3])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			resp = {"id":org[0], "name":org[1], "owner_id":org[2], "entry_fee":money, "description":org[4]}
			return json.dumps(resp)
	elif request.method == 'PUT':
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = id
		try:
			body['entry_fee'] = int(body['entry_fee'])
			cur.execute('UPDATE organizers SET name = %(name)s, entry_fee = %(entry_fee)s, owner_id = 1, description = %(description)s WHERE id=%(id)s', body)
			conn.commit()
			return Response(status=200)
		except (mysql.connector.Error, KeyError) as err:
			print(err)
			return Response(status=404)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM organizers WHERE id=%d' % id)
		if (cur.fetchone() is None):
			return Response(status=404)
		else:
			cur.execute('DELETE FROM organizers WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)	

#team routes
@app.route("/teams", methods=['GET', 'POST'])
def teams():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all teams
		resp = []
		cur.execute("SELECT * FROM teams")
		team = cur.fetchall()
		print(team)
		print(team[1][0])
		for a in range(len(team)):
			resp.append({"id":team[a][0], "name":team[a][1], "owner_id":team[a][2], "description":team[a][3]}) # had to make a new array because you can't change tuple values
		return json.dumps(resp)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		try: 
			cur.execute('INSERT INTO teams (name, owner_id, description) VALUES(%(name)s, 1, %(description)s)', body)
			conn.commit()
			return Response(status=200)
		except (mysql.connector.Error, KeyError) as err:
			print(err)
			return Response(status=404)

@app.route("/teams/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def showteam(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get team
		cur.execute("SELECT * FROM teams WHERE id=%d" % id)
		team = cur.fetchone()
		resp = ''
		if (team is None):
			resp = Response(status=404)
			return resp
		else:
			resp = {"id":team[0], "name":team[1], "owner_id":team[2], "description":team[3]}
			return json.dumps(resp)
	elif request.method == 'PUT':
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = id
		try:
			cur.execute('UPDATE teams SET name = %(name)s, owner_id = 1, description = %(description)s WHERE id=%(id)s', body)
			conn.commit()
			return Response(status=200)
		except (mysql.connector.Error, KeyError) as err:
			print(err)
			return Response(status=404)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM teams WHERE id=%d' % id)
		if (cur.fetchone() is None):
			return Response(status=404)
		else:
			cur.execute('DELETE FROM teams WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)			