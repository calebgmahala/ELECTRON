from flask import Flask, make_response, request, redirect, jsonif
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
@app.route("/leagues", methods=['GET'])
def leagues():
	if request.method == 'GET':
		# get all organizers
		cur.execute("SELECT * FROM organizers")
		org = cur.fetchall()
		money = str(org[0][3])[:-2] + "." + str(org[0][3])[-2:] #change entry fee from cent int to string decimal (used to display in json)
		resp = [org[0][0], org[0][1], org[0][2], money, org[0][4]] #change entry fee value to the string (had to make a new array because you can't change tuple value)
		return jsonify(resp)