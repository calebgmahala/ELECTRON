from flask import Flask, make_response, request, redirect, Response
# using flask as api framework
import mysql.connector
#used to pull mysql database
from flask_cors import CORS, cross_origin
#used to allow requests
import simplejson as json
#used to decode and encode json
import os
#used for encryption and key generation
import bcrypt
import string
import random

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
cors = CORS(app)
env = 'csx'

#connect to mysql database
def connect_db():
	return mysql.connector.connect(user='root', database=env, host='35.237.92.34', password='63099grant')

#show results function
def show_results(keys, obj, resp, respit=None, notkeys=[]):
	for b in range(len(keys)):
		if respit is None :
			if keys[b] not in notkeys:
				obj[keys[b]] = resp[b]
		else:
			if keys[b] not in notkeys:
				obj[keys[b]] = resp[respit][b]

# put post function
def put_post(var, notkeys, inserts, putpost):
	if putpost == 'POST':
		keys = '('
		value = ") VALUES("
		for i in range(len(var)):
			if var[i] not in notkeys:
				keys = keys + var[i] + ", "
				value = value + "'" + str(inserts[var[i]]) + "', "
		resp = keys[:-2] + value[:-2] + ")"
		return(resp)
	elif putpost == 'PUT':
		value = ''
		for i in range(len(var)):
			if var[i] not in notkeys and var[i] in inserts:
				value = value + str(var[i]) + " = '" + str(inserts[var[i]]) + "', "
		resp = value[:-2]
		return(resp)

# check auth function
def check_auth(table, key, field, perms):
	authpass = False
	if perms is not None:
		cur.execute('SELECT ' + str(key) + ' FROM ' + str(table) + ' WHERE ' + str(field) + '=' + str(perms))
		values = cur.fetchall()
		if request.headers.get(key) is not None:
			for i in values:
				if i[0] is not None:
					if bcrypt.checkpw(request.headers.get(key).encode("utf-8"), i[0].encode("utf-8")):
						authpass = True
						break
	return authpass

# gen key function
# credits to https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
def key_gen(size=12, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))

#set connection and cursor variables\
conn = connect_db()
cur = conn.cursor()

#keys for tables
league_keys = [
	'id',
	'name',
	'owner_id',
	'organizer_key',
	'entry_fee',
	'description']
team_keys = [
	'id',
	'name',
	'team_key',
	'description']
organizer_team_keys = [
	'id',
	'organizer_id',
	'team_id',
	'request']
tournament_keys = [
	'id',
	'organizer_id',
	'name',
	'type',
	'size',
	'start_date',
	'end_date',
	'entry_fee',
	'description']
user_keys = [
	'id',
	'username',
	'password',
	'request_key',
	'permission',
	'team_id',
	'is_owner_team',
	'description',
	'role']
bracket_keys = [
	'id',
	'tournament_id',
	'team_id',
	'place',
	'games_won',
	'games_tied',
	'games_lost',
	'score'
]

@app.route("/", methods=['GET'])
def home():
	return 'hello world'

#users routes
@app.route("/users", methods=['GET', 'POST'])
def Users():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all users
		resp = []
		cur.execute("SELECT * FROM users")
		usr = cur.fetchall()
		for a in range(len(usr)):
			obj = {}
			show_results(user_keys, obj, usr, a, ['password', 'request_key'])
			resp.append(obj)
		return json.dumps(resp)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		try: 
			body['password'] = bcrypt.hashpw( body['password'].encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
			cur.execute('INSERT INTO users ' + put_post(user_keys, ['id', 'request_key', 'permission', 'team_id', 'is_owner_team', 'description', 'role'], body, 'POST'))
			conn.commit()
			return Response(status=200)
		except (mysql.connector.Error, KeyError) as err:
			return Response(status=404)

@app.route("/users/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def User(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get user
		cur.execute("SELECT * FROM users WHERE id=%d" % id)
		usr = cur.fetchone()
		resp = {}
		if (usr is None):
			resp = Response(status=404)
			return resp
		else:
			show_results(user_keys, resp, usr, notkeys=['password', 'request_key'])
			return json.dumps(resp)
	elif request.method == 'PUT':
		cur.execute('SELECT * FROM users WHERE id='+str(id))
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = id
		if cur.fetchone() is None:
			return Response(status=404)
		elif check_auth('users', 'request_key', 'id', id) and check_auth('teams', 'team_key', 'id', request.headers.get('team_id')):
			cur.execute('UPDATE users SET team_id=' + request.headers.get('team_id') + ' WHERE id=' + str(body['id']))
			conn.commit()
			return Response(status=200)
		elif len(request.form) is 0:
			return Response(status=409)
		elif check_auth('users', 'request_key', 'permission', 2):
			cur.execute('UPDATE users SET ' + put_post(user_keys, ['id'], body, 'PUT') + ' WHERE id=' + str(body['id']))
			conn.commit()
			return Response(status=200)
		elif check_auth('users', 'request_key', 'id', id):
			cur.execute('UPDATE users SET ' + put_post(user_keys, ['id', 'request_key', 'permission', 'team_id', 'is_owner_team'], body, 'PUT') + ' WHERE id=' + str(body['id']))
			conn.commit()
			return Response(status=200)
		else:
			return Response(status=409)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM users WHERE id=%d' % id)
		if (cur.fetchone() is None):
			return Response(status=404)
		elif not check_auth('users', 'request_key', 'id', id) and not check_auth('users', 'request_key', 'id', 'team_id'):
			return Response(status=409)
		else:
			cur.execute('DELETE FROM brackets WHERE 1=1')
			cur.execute('DELETE FROM organizers_teams WHERE organizer_id=%d' % id)
			cur.execute('DELETE FROM tournaments WHERE organizer_id=%d' % id )			
			cur.execute('DELETE FROM organizers WHERE id=%d' % id )
			cur.execute('DELETE FROM users WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)	

@app.route("/login", methods=['POST', 'DELETE'])
def Login():
	if request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		cur.execute("SELECT * FROM users WHERE username='" + str(body['username']) + "'")
		usr = cur.fetchone()
		resp = {}
		if (usr is None or not bcrypt.checkpw(body['password'].encode("utf-8"), usr[2].encode("utf-8"))):
			resp = Response(status=404)
			return resp
		else:
			show_results(user_keys, resp, usr, notkeys=['password', 'description', 'team_id', 'request_key', 'is_owner_team', 'role'])
			key = key_gen()
			resp['request_key'] = key
			hashedkey = bcrypt.hashpw( key.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
			cur.execute("UPDATE users SET request_key='" + str(hashedkey) + "' WHERE id=" + str(resp['id']))
			conn.commit()
			return json.dumps(resp)
	elif request.method == 'DELETE':
		body = json.dumps(request.form)
		body = json.loads(body)
		cur.execute("SELECT * FROM users WHERE id="+str(body['id']))
		usr = cur.fetchone()
		if usr is None:
			return Response(status=404)
		elif check_auth('users', 'request_key', 'id', str(body['id'])):
			cur.execute("UPDATE users SET request_key=0 WHERE id="+str(body['id']))
			conn.commit()
			return Response(status=200)
		else:
			return Response(status=409)

#league routes
@app.route("/leagues", methods=['GET', 'POST'])
def Leagues():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all organizers
		resp = []
		cur.execute("SELECT * FROM organizers")
		org = cur.fetchall()
		for a in range(len(org)):
			obj = {}
			show_results(league_keys, obj, org, a, ['organizer_key'])
			money = str(obj['entry_fee'])[:-2] + "." + str(obj['entry_fee'])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			obj['entry_fee'] = money
			resp.append(obj)
		return json.dumps(resp)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		if check_auth('users', 'request_key', 'permission', 1) or check_auth('users', 'request_key', 'permission', 2):
			try: 
				body['organizer_key'] = bcrypt.hashpw( body['organizer_key'].encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
				body['entry_fee'] = int(body['entry_fee'])
				cur.execute('INSERT INTO organizers ' + put_post(league_keys, ['id'], body, 'POST'))
				conn.commit()
				return Response(status=200)
			except (mysql.connector.Error, KeyError) as err:
				return Response(status=404)
		else:
			return Response(status=409)

@app.route("/leagues/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def League(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		org = cur.fetchone()
		resp = {}
		if (org is None):
			resp = Response(status=404)
			return resp
		else:
			show_results(league_keys, resp, org, notkeys=['organizer_key'])
			money = str(resp['entry_fee'])[:-2] + "." + str(resp['entry_fee'])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			resp['entry_fee'] = money
			return json.dumps(resp)
	elif request.method == 'PUT':
		cur.execute('SELECT * FROM organizers WHERE id='+str(id))
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = id
		if cur.fetchone() is None:
			return Response(status=404)
		elif check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id=' + str(id) + ')') or check_auth('users', 'request_key', 'permission', 2):
			try:
				body['organizer_key'] = bcrypt.hashpw( body['organizer_key'].encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
			except:
				pass
			body['entry_fee'] = int(body['entry_fee'])
			cur.execute('UPDATE organizers SET ' + put_post(league_keys, ['id'], body, 'PUT') + ' WHERE id=' + str(body['id']))
			conn.commit()
			return Response(status=200)
		else:
			return Response(status=409)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM organizers WHERE id=%d' % id)
		if (cur.fetchone() is None):
			return Response(status=404)
		elif check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id=' + str(id) + ')') or check_auth('users', 'request_key', 'permission', 2):
			cur.execute('DELETE FROM brackets WHERE 1=1')
			cur.execute('DELETE FROM organizers_teams WHERE organizer_id=%d' % id)
			cur.execute('DELETE FROM tournaments WHERE organizer_id=%d' % id )			
			cur.execute('DELETE FROM organizers WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)
		else:	
			return Response(status=409)

@app.route("/leagues/<int:id>/teams", methods=['GET', 'POST'])
def LeagueTeams(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM teams WHERE id IN (SELECT team_id FROM organizers_teams WHERE organizer_id=%d AND request=0)" % id)
		team = cur.fetchall()
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		league = cur.fetchall()
		resp = []
		if (league == []):
			resp = Response(status=404)
			return resp
		else:
			for a in range(len(team)):
				obj = {}
				show_results(team_keys, obj, team, a, ['team_key'])
				resp.append(obj)
			return json.dumps(resp)	
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		if check_auth('users', 'request_key', 'team_id', str(body['team_id']) + ' AND is_owner_team=1'):
			try: 
				cur.execute('INSERT INTO organizers_teams ' + put_post(organizer_team_keys, ['id','request'], body, 'POST'))
				conn.commit()
				return Response(status=200)
			except (mysql.connector.Error, KeyError) as err:
				return Response(status=404)
		else:
			return Response(status=409)

@app.route("/leagues/<int:id>/teams/requests", methods=['GET', 'POST'])
def LeagueTeamsRequests(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM teams WHERE id IN (SELECT team_id FROM organizers_teams WHERE organizer_id=%d AND request=1)" % id)
		team = cur.fetchall()
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		league = cur.fetchall()
		resp = []
		if (league == []):
			resp = Response(status=404)
			return resp
		else:
			for a in range(len(team)):
				obj = {}
				show_results(team_keys, obj, team, a, ['team_key'])
				resp.append(obj)
			return json.dumps(resp)	
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		if check_auth('users', 'request_key', 'team_id', str(body['team_id']) + ' AND is_owner_team=1'):
			try: 
				cur.execute('INSERT INTO organizers_teams ' + put_post(organizer_team_keys, ['id','request'], body, 'POST'))
				conn.commit()
				return Response(status=200)
			except (mysql.connector.Error, KeyError) as err:
				return Response(status=404)
		else:
			return Response(status=409)

@app.route("/leagues/<int:org_id>/teams/<int:t_id>", methods=['GET', 'PUT', 'DELETE'])
def LeagueTeam(org_id, t_id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		cur.execute("SELECT * FROM organizers_teams WHERE organizer_id="+str(org_id)+" AND team_id="+str(t_id))
		team = cur.fetchone()
		resp = {}
		if (team is None):
			resp = Response(status=404)
			return resp
		else:
			show_results(organizer_team_keys, resp, team)
			return json.dumps(resp)
	elif request.method == 'PUT':
		body = json.dumps(request.form)
		body = json.loads(body)
		cur.execute("SELECT * FROM organizers_teams WHERE organizer_id="+str(org_id)+" AND team_id="+str(t_id))
		team = cur.fetchone()
		if team is not None:
			body['id'] = team[0]
			if check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id=' + str(org_id) + ')') or check_auth('organizers', 'organizer_key', 'id', str(org_id)):
				cur.execute('UPDATE organizers_teams SET ' + put_post(organizer_team_keys, ['id','organizer_id','team_id'], body, 'PUT') + ' WHERE id=' + str(body['id']))
				conn.commit()
				return Response(status=200)			
			else:
				return Response(status=409)
		else:
			return Response(status=404)
	elif request.method == 'DELETE':
		if check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id=' + str(org_id) + ')') or check_auth('users', 'request_key', 'team_id', str(t_id) + ' AND is_owner_team=1') or check_auth('organizers', 'organizer_key', 'id', str(org_id)):
			cur.execute('SELECT * FROM teams WHERE id='+str(t_id))
			if (cur.fetchone() is None):
				return Response(status=404)
			else:
				cur.execute('DELETE FROM organizers_teams WHERE team_id='+str(t_id)+' AND organizer_id='+str(org_id))
				conn.commit()
				return Response(status=200)
		else:
			return Response(status=409)

@app.route("/leagues/<int:id>/tournaments", methods=['GET'])
def LeagueTournaments(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM tournaments WHERE organizer_id=%d" % id)
		trn = cur.fetchall()
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		league = cur.fetchall()
		resp = []
		if (league == []):
			resp = Response(status=404)
			return resp
		else:
			for a in range(len(trn)):
				obj = {}
				show_results(tournament_keys, obj, trn, a)
				money = str(obj['entry_fee'])[:-2] + "." + str(obj['entry_fee'])[-2:] #change entry fee from cent int to string decimal (used to display in json)
				obj['entry_fee'] = money
				resp.append(obj)
			return json.dumps(resp, default=str)

#team routes
@app.route("/teams", methods=['GET', 'POST'])
def Teams():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all teams
		resp = []
		cur.execute("SELECT * FROM teams")
		team = cur.fetchall()
		for a in range(len(team)):
			obj = {}
			show_results(team_keys, obj, team, a, ['team_key'])
			resp.append(obj)		
		return json.dumps(resp)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		if 'user_id' not in body.keys():
			return Response(status=404)
		elif check_auth('users', 'request_key', 'id', str(body['user_id'])):
			try:
				body['team_key'] = bcrypt.hashpw( body['team_key'].encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
				cur.execute('INSERT INTO teams ' + put_post(team_keys, ['id'], body, 'POST'))
				cur.execute('SELECT LAST_INSERT_ID()')
				team = cur.fetchone()
				cur.execute("UPDATE users SET team_id="+str(team[0])+", is_owner_team=1 WHERE id="+body['user_id'])
				conn.commit()
				return Response(status=200)
			except (mysql.connector.Error, KeyError) as err:
				return Response(status=404)
		else:
			return Response(status=409)

@app.route("/teams/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def Team(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		print(id)
		# get team
		cur.execute("SELECT * FROM teams WHERE id=%d" % id)
		team = cur.fetchone()
		resp = {}
		if (team is None):
			resp = Response(status=404)
			return resp
		else:
			show_results(team_keys, resp, team, notkeys=['team_key'])
			print('done')
			return json.dumps(resp)
	elif request.method == 'PUT':
		cur.execute('SELECT * FROM teams WHERE id='+str(id))
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = id
		if cur.fetchone() is None:
			return Response(status=404)
		elif check_auth('users', 'request_key', 'team_id', str(id)+' AND is_owner_team=1'):
			try:
				body['team_key'] = bcrypt.hashpw( body['team_key'].encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
			except:
				pass
			cur.execute('UPDATE teams SET ' + put_post(team_keys, ['id'], body, 'PUT') + ' WHERE id=' + str(body['id']))
			conn.commit()
			return Response(status=200)
		else:
			return Response(status=409)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM teams WHERE id=%d' % id)
		if (cur.fetchone() is None):
			return Response(status=404)
		elif check_auth('users', 'request_key', 'team_id', str(id)+' AND is_owner_team=1'):
			cur.execute('DELETE FROM brackets WHERE 1=1')
			cur.execute('DELETE FROM organizers_teams WHERE team_id='+str(id))
			cur.execute('UPDATE users SET team_id=Null WHERE team_id='+str(id))
			cur.execute('DELETE FROM teams WHERE id='+str(id))
			conn.commit()
			return Response(status=200)
		else:
			return Response(status=409)

@app.route("/teams/<int:id>/leagues", methods=['GET', 'DELETE'])
def TeamLeagues(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM organizers WHERE id IN (SELECT organizer_id FROM organizers_teams WHERE team_id=%d)" % id)
		team = cur.fetchall()
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		league = cur.fetchall()
		resp = []
		if (league == []):
			resp = Response(status=404)
			return resp
		else:
			for a in range(len(team)):
				obj = {}
				show_results(league_keys, obj, team, a, ['organizer_key'])
				resp.append(obj)
			return json.dumps(resp)
	elif request.method == 'DELETE':
		if check_auth('users', 'request_key', 'team_id', str(id) + ' AND is_owner_team=1'):
			cur.execute('SELECT * FROM teams WHERE id=%d' % t_id)
			if (cur.fetchone() is None):
				return Response(status=404)
			else:
				cur.execute('DELETE FROM organizers_teams WHERE team_id='+str(t_id)+' AND organizer_id='+str(org_id))
				conn.commit()
				return Response(status=200)
		else:
			return Response(status=409)	

# tournament routes
@app.route("/tournaments", methods=['GET', 'POST'])
def Tournaments():
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all organizers
		resp = []
		cur.execute("SELECT * FROM tournaments")
		trn = cur.fetchall()
		for a in range(len(trn)):
			money = str(trn[a][7])[:-2] + "." + str(trn[a][7])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			obj = {}
			show_results(tournament_keys, obj, trn, a)
			obj['entry_fee'] = money
			resp.append(obj)
		return json.dumps(resp, default=str)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		if 'organizer_id' not in body.keys():
			return Response(status=404)
		elif check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id =' + body['organizer_id'] + ')') or check_auth('organizers', 'organizer_key', 'id', body['organizer_id']):
			try: 
				body['entry_fee'] = int(body['entry_fee'])
				cur.execute('INSERT INTO tournaments ' + put_post(tournament_keys, ['id', 'end_date'], body, 'POST'))
				conn.commit()
				return Response(status=200)
			except (mysql.connector.Error, KeyError) as err:
				return Response(status=404)
		else:
			return Response(status=409)
			
@app.route("/tournaments/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def Tournament(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM tournaments WHERE id=%d" % id)
		trn = cur.fetchone()
		resp = {}
		if (trn is None):
			resp = Response(status=404)
			return resp
		else:
			show_results(tournament_keys, resp, trn)
			money = str(resp['entry_fee'])[:-2] + "." + str(resp['entry_fee'])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			resp['entry_fee'] = money
			return json.dumps(resp, default=str)
	elif request.method == 'PUT':
		cur.execute("SELECT * FROM tournaments WHERE id=%d" % id)
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = id
		if cur.fetchone() is None:
			return Response(status=404)
		elif check_auth('organizers', 'organizer_key', 'id', str(id)) or check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id =(SELECT organizer_id FROM tournaments WHERE id=' + str(id) +')) OR permission=2'):
			body['entry_fee'] = int(body['entry_fee'])
			cur.execute("UPDATE tournaments SET " + put_post(tournament_keys, ['id'], body, 'PUT') + " WHERE id=" + str(body['id']))
			conn.commit()
			return Response(status=200)
		else:
			return Response(status=409)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM tournaments WHERE id=%d' % id)
		if (cur.fetchone() is None):
			return Response(status=404)
		elif check_auth('organizers', 'organizer_key', 'id', str(id)) or check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id =(SELECT organizer_id FROM tournaments WHERE id=' + str(id) +')) OR permission=2'):
			cur.execute('DELETE FROM brackets WHERE 1=1')
			cur.execute('DELETE FROM tournaments WHERE id=%d' % id )
			conn.commit()
			return Response(status=200)	
		else:
			return Response(status=409)

@app.route("/tournaments/<int:id>/brackets", methods=['GET', 'POST'])
def Brackets(id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get all brackets
		resp = []
		cur.execute("SELECT * FROM brackets ORDER BY place")
		brak = cur.fetchall()
		for a in range(len(brak)):
			obj = {}
			show_results(bracket_keys, obj, brak, a)
			obj['games_played'] = obj['games_won']+obj['games_tied']+obj['games_lost']
			resp.append(obj)	
		return json.dumps(resp)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		body = json.loads(body)
		if check_auth('organizers', 'organizer_key', 'id', '(SELECT organizer_id FROM tournaments WHERE id=' + str(id) + ')') or check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id =(SELECT organizer_id FROM tournaments WHERE id=' + str(id) +'))'):
			try: 
				cur.execute('INSERT INTO brackets ' + put_post(bracket_keys, ['id', 'games_won', 'games_tied', 'games_lost', 'score'], body, 'POST'))
				conn.commit()
				return Response(status=200)
			except (mysql.connector.Error, KeyError) as err:
				return Response(status=404)
		else:
			return Response(status=409)

@app.route("/tournaments/<int:t_id>/brackets/<int:brak_id>", methods=['GET', 'PUT', 'DELETE'])
def Bracket(t_id, brak_id):
	conn.commit() # allows reload for testing otherwise database is not refreshed
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM brackets WHERE id="+str(brak_id))
		brak = cur.fetchone()
		resp = {}
		if (brak is None):
			resp = Response(status=404)
			return resp
		else:
			show_results(bracket_keys, resp, brak)
			resp['games_played'] = resp['games_won']+resp['games_tied']+resp['games_lost']
			return json.dumps(resp)
	elif request.method == 'PUT':
		cur.execute('SELECT * FROM brackets WHERE id='+str(brak_id))
		body = json.dumps(request.form)
		body = json.loads(body)
		body['id'] = brak_id
		if cur.fetchone() is None:
			return Response(status=404)
		elif check_auth('organizers', 'organizer_key', 'id', '(SELECT organizer_id FROM tournaments WHERE id=' + str(t_id) + ')') or check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id =(SELECT organizer_id FROM tournaments WHERE id=' + str(t_id) +'))'):
			cur.execute('UPDATE brackets SET ' + put_post(bracket_keys, ['id'], body, 'PUT') + ' WHERE id=' + str(body['id']))
			conn.commit()
			return Response(status=200)
		else:
			return Response(status=409)
	elif request.method == 'DELETE':
		cur.execute('SELECT * FROM brackets WHERE id=' + str(brak_id))
		if (cur.fetchone() is None):
			return Response(status=404)
		elif check_auth('organizers', 'organizer_key', 'id', '(SELECT organizer_id FROM tournaments WHERE id=' + str(t_id) + ')') or check_auth('users', 'request_key', 'id', '(SELECT owner_id FROM organizers WHERE id =(SELECT organizer_id FROM tournaments WHERE id=' + str(t_id) +'))'):
			cur.execute('DELETE FROM brackets WHERE id='+str(brak_id))
			conn.commit()
			return Response(status=200)
		else:	
			return Response(status=409)