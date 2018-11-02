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

#show results function
def show_results(keys, obj, resp, respit=None):
	for b in range(len(keys)):
		if respit is None :
			obj[keys[b]] = resp[b]
		else:	
			obj[keys[b]] = resp[respit][b]

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
		keys = [
			'id',
			'name',
			'owner_id',
			'entry_fee',
			'description'
			]
		for a in range(len(org)):
			money = str(org[a][3])[:-2] + "." + str(org[a][3])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			obj = {}
			show_results(keys, obj, org, a)
			obj['entry_fee'] = money
			resp.append(obj)
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
def showLeague(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		org = cur.fetchone()
		keys = [
			'id',
			'name',
			'owner_id',
			'entry_fee',
			'description'
			]
		resp = {}
		if (org is None):
			resp = Response(status=404)
			return resp
		else:
			money = str(org[3])[:-2] + "." + str(org[3])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			show_results(keys, resp, org)
			resp['entry_fee'] = money
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
			cur.execute('DELETE FROM organizers_teams WHERE organizer_id=%d' % id)
			cur.execute('DELETE FROM tournaments WHERE organizer_id=%d' % id )			
			cur.execute('DELETE FROM organizers WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)	

@app.route("/leagues/<int:id>/teams", methods=['GET', 'PUT', 'DELETE'])
def showLeagueTeams(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM teams WHERE id IN (SELECT team_id FROM organizers_teams WHERE organizer_id=%d)" % id)
		team = cur.fetchall()
		keys = [
			'id',
			'name',
			'owner_id',
			'description'
			]
		resp = []
		for a in range(len(team)):
			obj = {}
			show_results(keys, obj, team, a)
			resp.append(obj)
		return json.dumps(resp)		

@app.route("/leagues/<int:id>/tournaments", methods=['GET', 'PUT', 'DELETE'])
def showTournamentsOfLeague(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM tournaments WHERE organizer_id=%d" % id)
		trn = cur.fetchall()
		keys = [
			'id',
			'organizer_id',
			'name',
			'type',
			'size',
			'start_date',
			'end_date',
			'entry_fee',
			'description'
			]
		resp = []
		for a in range(len(trn)):
			money = str(trn[a][7])[:-2] + "." + str(trn[a][7])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			obj = {}
			show_results(keys, obj, trn, a)
			obj['entry_fee'] = money
			resp.append(obj)
		return json.dumps(resp, default=str)

#team routes
@app.route("/teams", methods=['GET', 'POST'])
def teams():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all teams
		resp = []
		cur.execute("SELECT * FROM teams")
		team = cur.fetchall()
		keys = [
			'id',
			'name',
			'owner_id',
			'description'
			]
		for a in range(len(team)):
			obj = {}
			show_results(keys, obj, team, a)
			resp.append(obj)		
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
def showTeam(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get team
		cur.execute("SELECT * FROM teams WHERE id=%d" % id)
		team = cur.fetchone()
		keys = [
			'id',
			'name',
			'owner_id',
			'description'
			]
		resp = {}
		if (team is None):
			resp = Response(status=404)
			return resp
		else:
			show_results(keys, resp, team)
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
			cur.execute('DELETE FROM organizers_teams WHERE team_id=%d' % id)
			cur.execute('DELETE FROM teams WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)	

@app.route("/teams/<int:id>/leagues", methods=['GET', 'PUT', 'DELETE'])
def showTeamLeagues(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM organizers WHERE id IN (SELECT organizer_id FROM organizers_teams WHERE team_id=%d)" % id)
		team = cur.fetchall()
		keys = [
			'id',
			'name',
			'owner_id',
			'entry_fee',
			'description'
			]
		resp = []
		for a in range(len(team)):
			obj = {}
			show_results(keys, obj, team, a)
			resp.append(obj)
		return json.dumps(resp)		

# tournament routes
@app.route("/tournaments", methods=['GET', 'POST'])
def tournaments():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all organizers
		resp = []
		cur.execute("SELECT * FROM tournaments")
		trn = cur.fetchall()
		keys = [
			'id',
			'organizer_id',
			'name',
			'type',
			'size',
			'start_date',
			'end_date',
			'entry_fee',
			'description'
			]
		for a in range(len(trn)):
			money = str(trn[a][7])[:-2] + "." + str(trn[a][7])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			obj = {}
			show_results(keys, obj, trn, a)
			obj['entry_fee'] = money
			resp.append(obj)
		return json.dumps(resp, default=str)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		try: 
			body['entry_fee'] = int(body['entry_fee'])
			cur.execute('INSERT INTO tournaments (organizer_id, name, type, size, start_date, entry_fee, description) VALUES(1, %(name)s, %(type)s, %(size)s, %(start_date)s, %(entry_fee)s, %(description)s)', body)
			conn.commit()
			return Response(status=200)
		except (mysql.connector.Error, KeyError) as err:
			print(err)
			return Response(status=404)

@app.route("/tournaments/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def showTournament(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM tournaments WHERE id=%d" % id)
		trn = cur.fetchone()
		keys = [
			'id',
			'organizer_id',
			'name',
			'type',
			'size',
			'start_date',
			'end_date',
			'entry_fee',
			'description'
			]
		resp = {}
		if (trn is None):
			resp = Response(status=404)
			return resp
		else:
			money = str(trn[7])[:-2] + "." + str(trn[7])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			show_results(keys, resp, trn)
			resp['entry_fee'] = money
			return json.dumps(resp, default=str)
	elif request.method == 'PUT':
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = id
		try:
			body['entry_fee'] = int(body['entry_fee'])
			cur.execute('UPDATE tournaments SET name = %(name)s, type = %(type)s, size = %(size)s, start_date = %(start_date)s, end_date = %(end_date)s, entry_fee = %(entry_fee)s, description = %(description)s WHERE id=%(id)s', body)
			conn.commit()
			return Response(status=200)
		except (mysql.connector.Error, KeyError) as err:
			print(err)
			return Response(status=404)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM tournaments WHERE id=%d' % id)
		if (cur.fetchone() is None):
			return Response(status=404)
		else:
			cur.execute('DELETE FROM tournaments WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)	

# league to team routes