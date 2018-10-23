from flask import Flask, make_response, request, redirect, jsonify
# using flask as api framework
from flaskext.mysql import MySQL
#used to pull mysql database
import os

#connect to mysql database
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'csx'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)

#set connection and cursor variables
conn =  mysql.connect()
cur = conn.cursor()

#league routes
@app.route("/leagues", methods=['GET', 'POST'])
def leagues():
	if request.method == 'GET':
		# get all organizers
		cur.execute("SELECT * FROM organizers")
		org = cur.fetchall()
		resp = []
		for a in range(len(org)):
			money = str(org[a][3])[:-2] + "." + str(org[a][3])[-2:] #change entry fee from cent int to string decimal (used to display in json)
			resp.append({"id":org[a][0], "name":org[a][1], "owner_id":org[a][2], "entry_fee":money, "desc":org[a][4]}) # change entry fee value to the string (had to make a new array because you can't change tuple values)
		return jsonify(resp)
	elif request.method == 'POST':
		body = json.dumps(request.form)
		cur.execute('INSERT INTO leagues (name, entry_fee, desc) VALUES(%(name)s, %(entry_fee)s, %(desc)s)', json.loads(body))
		conn.commit()
		return redirect('localhost:5000/leagues', code=200)

@app.route("/leagues/<int:id>", methods=['GET'])
def showleague(id):
	if request.method == 'GET':
		# get organizer
		cur.execute("SELECT * FROM organizers WHERE id=%d" % id)
		org = cur.fetchone()
		money = str(org[3])[:-2] + "." + str(org[3])[-2:] #change entry fee from cent int to string decimal (used to display in json)
		resp = {"id":org[0], "name":org[1], "owner_id":org[2], "entry_fee":money, "desc":org[4]}
		return jsonify(resp)