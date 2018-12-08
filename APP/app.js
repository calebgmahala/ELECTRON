// express is main framework
const express = require('express')
const app = express()
app.use(express.static('public'))
const port = 3000

// require is used to send out api requests
const request = require('request')

// mustache is template handler
const mustache = require('mustache-express')
app.engine('html', mustache())
app.set('view engine', 'html')
app.set('views', __dirname + '/views')

// sesions
const session = require('express-session');
const bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(session({secret: "I play pokemon go everyday", resave: false, saveUninitialized: true}));

templateVar = {}

//  api request function
function CallApi(a, b='GET') {
	var resp = ''
	return new Promise(function(resolve, reject){
	    request({url: 'http://localhost:5000/'+a, method: b}, function (error, response, body) {
	    	if (!error && response.statusCode == 200) {
	    		resolve(body)
	  		} else if (response.statusCode == 404) {
	  			resolve(null)
	  		} else {
	  			reject(Error(error + " | " + response + " | " + body))
	  		}
		})
	})
}

function resetTempVar() {
	var resp = {}
	resp['user'] = templateVar["user"]
	resp['id'] = templateVar["id"]
	resp['key'] = templateVar["key"]
	resp['perms'] = templateVar["perms"]

	return resp
}

function roles(user) {
	if (user['role'] == 1) {
		return 'rifler'
	} else if (user['role'] == 2) {
		return 'awper'
	} else{
		return 'undefined'
	}
}

function types(tourn) {
	if (tourn['type'] == 1) {
		return 'league'
	} else if (tourn['type'] == 2) {
		return 'tournament'
	} else{
		return 'undefined'
	}
}

// login and users
app.get('/login', function(req, res) {
	templateVar = resetTempVar()
	templateVar["user"] = req.session.user 
	templateVar["id"] = req.session.user_id
	templateVar["key"] = req.session.key
	templateVar['file'] = 'login.js'
	templateVar['title'] = 'Login'
	res.render('login.html', templateVar)
})

app.post('/login', function(req, res) {
	var body = req.body
    request({
    	method: 'POST',
    	url: 'http://localhost:5000/login',
    	form: body,
    	json: true}, function(error, response, body){
		if (!error && response.statusCode == 200) {
    		req.session.user = body['username']
    		req.session.user_id = body['id']
    		req.session.key = body['request_key']
    		templateVar["user"] = body['username']
    		templateVar["id"] = body['id']
    		templateVar["key"] = body['request_key']
    		templateVar["perms"] = body['permission']
			res.status(200)
			res.send(body['id'].toString())
  		} else {
  			res.sendStatus(404)
  		}
	});
})

app.get('/logout', function(req, res) {
	var body = req.body
	var key = req.headers
    request({
    	method: 'DELETE',
    	url: 'http://localhost:5000/login',
    	form: {'id': req.session.user_id},
    	headers: {'request_key': req.session.key}}, function(error, response, body){
		if (!error && response.statusCode == 200) {
    		req.session.destroy()
    		templateVar = {}
			res.sendStatus(200) 
  		} else {
  			res.sendStatus(404)
  		}
	});
})

app.get('/signup', function(req, res) {
	templateVar = resetTempVar()
	templateVar['file'] = 'signup.js'
	templateVar['title'] = 'Signup'
	res.render('login.html', templateVar)
})

app.get('/users', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('users').then(function(users) {
		users = JSON.parse(users)
		templateVar = resetTempVar()
		templateVar['title'] = 'Users'
		templateVar['users'] = users
		for (var a in users) {
			templateVar['users'][a]['role'] = roles(users[a])
			// CallApi('teams/'+users[a]['team_id']).then(function(team) {
			// 	team = JSON.parse(team)
			// 	console.log(team['name'])
			// 	templateVar['users'][a]['team_name'] = team['name']
			// })
		}
			res.render('users.html', templateVar)
	})
})

app.get('/user/:id', async function(req, res) {
	var promiseArray = []
	var resp = {}
	resp['user'] = []
	resp['team'] = []
	resp['leagues'] = []
	// make an api call and on response render the html page.
	var prom0 = CallApi('users/'+req.params['id'])
	promiseArray.push(prom0)
	await prom0.then(async function(user) {
		user = JSON.parse(user)
		resp['user'] = user
		user['matches'] = []
		user['match_stats'] = []
		if (user['team_id'] != null) {
			var prom1 = CallApi('teams/'+user['team_id'])
			promiseArray.push(prom1)
			await prom1.then(async function(team) {
				team = JSON.parse(team)
				resp['team'] = team
				var prom2 = CallApi('teams/'+user['team_id']+'/leagues')
				promiseArray.push(prom2)
				await prom2.then(async function(leagues) {
					leagues = JSON.parse(leagues)
					resp['leagues'] = leagues
					for (var i in leagues) {
						if (leagues[i]) {
							var prom3 = CallApi('leagues/'+leagues[i]['id']+'/tournaments')
							promiseArray.push(prom3)
							await prom3.then(async function(tournaments) {
								resp['leagues'] = leagues
								leagues[i]['tournaments'] = JSON.parse(tournaments)
								for (var t in leagues[i]['tournaments']) {
									if (leagues[i]['tournaments'][t]) {
										var prom4 = CallApi('tournaments/'+leagues[i]['tournaments'][t]['id']+'/matches')
										promiseArray.push(prom4)
										await prom4.then(async function(matches) {
											leagues[i]['tournaments'][t]['matches'] = JSON.parse(matches)
											resp['leagues'] = leagues
											for (var m in leagues[i]['tournaments'][t]['matches']) {
												if (leagues[i]['tournaments'][t]['matches'][m]) {
													var prom5 = CallApi('matches/'+leagues[i]['tournaments'][t]['matches'][m]['id']+'/leaderboard')
													promiseArray.push(prom5)
													await prom5.then(function(match_leaderboards) {
														leagues[i]['tournaments'][t]['matches'][m]['match_leaderboards'] = JSON.parse(match_leaderboards)
														for (var ml in leagues[i]['tournaments'][t]['matches'][m]['match_leaderboards']) {
															if (leagues[i]['tournaments'][t]['matches'][m]['match_leaderboards'][ml]) {
																if (leagues[i]['tournaments'][t]['matches'][m]['match_leaderboards'][ml]['player_id'] == req.params['id']) {
																	user['matches'].push(leagues[i]['tournaments'][t]['matches'][m])
																	user['match_stats'].push(leagues[i]['tournaments'][t]['matches'][m]['match_leaderboards'][ml])
																}
																resp['user'] = user
																resp['team'] = team
																resp['leagues'] = leagues
															}
														}
													})
												}
											}
										})
									}
								}
							})
						}
					}						
				})
			})
		} else {
			resp['user'] = user
		}
	})
	await Promise.all(promiseArray).then(async function(value) {
		templateVar = resetTempVar()
		if (resp['user']['id'] == templateVar['id']) {
			templateVar['self'] = true;
		}
		if (templateVar['perms'] == 2) {
			templateVar['admin'] = true;
		}
		templateVar["files"] = ['logout.js', 'leaveTeam.js']
		templateVar['labels'] = []
		templateVar['title'] = 'Profile'
		templateVar['user_id'] = resp['user']['id']
		templateVar['username'] = resp['user']['username']
		templateVar['team_id'] = resp['user']['team_id']
		templateVar['team_name'] = resp['team']['name']
		templateVar['description'] = resp['user']['description']
		templateVar['role'] = roles(resp['user'])
		templateVar['matches'] = resp['user']['matches']
		for (i in templateVar['matches']) {
			templateVar['labels'].push(templateVar['matches'][i]['end_date'].split(' ')[0])
			await CallApi('teams/'+templateVar['matches'][i]['home_id']).then(async function(home) {
				await CallApi('teams/'+templateVar['matches'][i]['away_id']).then(function(away) {
					home = JSON.parse(home)
					away = JSON.parse(away)
					templateVar['matches'][i]['away_name'] = away['name']
					templateVar['matches'][i]['home_name'] = home['name']
				})
			})
		}	
		templateVar['match_stats'] = resp['user']['match_stats']
		for (i in templateVar['match_stats']) {
			if (templateVar['match_stats'][i]['deaths'] != 0) {
				templateVar['match_stats'][i]['k/d'] = templateVar['match_stats'][i]['kills']/templateVar['match_stats'][i]['deaths']
			} else {
				templateVar['match_stats'][i]['k/d'] = templateVar['match_stats'][i]['kills']
			}
		}
		res.render('user.html', templateVar)
	})
})

app.get('/user/:id/edit', async function(req, res) {
	CallApi('users/'+req.params['id']).then(function(user) {
		user = JSON.parse(user)
		templateVar['file'] = ['editUser.js']
		templateVar['title'] = 'Edit Profile'
		templateVar['description'] = user['description']
		res.render('userForm.html', templateVar)
	})
})

app.get('/user/:id/join', async function(req, res) {
	templateVar['file'] = 'joinTeam.js'
	templateVar['title'] = 'Join Team'
	res.render('joinTeam.html', templateVar)
})
// show all leagues
app.get('/leagues', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('leagues').then(function(value) {
		templateVar = resetTempVar()
		templateVar['title'] = 'Leagues'
		templateVar['leagues'] = JSON.parse(value)
		res.render('leagues.html', templateVar)	
	})
})

// show one leagues
app.get('/league/:id', function(req, res) {
	//function to make tournament cards
	function Card(a) {
		a = JSON.parse(a)// turn a into object otherwise it is a string
		string = "";
		for (var b in a) {
			string = string + "<div class='card'><h3><a href='/tournament/" + a[b]['id'] + "'>" + a[b]['name'] + "</a></h3>";
			string = string + "<p>" + a[b]['description'] + "</p>"
			string = string + "<p>$" + a[b]['entry_fee'] + "</p></div>"
		}
		return(string)
	}
	//function to make team table
	function TeamsTable(a) {
		a = JSON.parse(a)// turn a into object otherwise it is a string
		string = "<tr><th>Id</th><th>Name</th><th>Owner</th><th>Description</th><th>Actions</th></tr>";
		for (var b in a) {
			string = string + "<tr><td>"
			string = string + a[b]['id'] + "</td><td>"
			string = string + "<a href='/team/" + a[b]['id'] + "'>" + a[b]['name'] + "</a></td><td>"
			string = string + a[b]['owner_id'] + "</td><td>"
			string = string + a[b]['description'] + "</td><td>"
			string = string + "<button type=button value=" + a[b]['id'] + " class='removeLeagueTeam' data-key='{{key}}'>Kick</button></td></tr>"
		}
		return(string)
	}
	function RequestsTable(a) {
		a = JSON.parse(a)// turn a into object otherwise it is a string
		string = "<tr><th>Id</th><th>Name</th><th>Owner</th><th>Description</th><th>Actions</th></tr>";
		for (var b in a) {
			string = string + "<tr><td>"
			string = string + a[b]['id'] + "</td><td>"
			string = string + "<a href='/teams/" + a[b]['id'] + "'>" + a[b]['name'] + "</a></td><td>"
			string = string + a[b]['owner_id'] + "</td><td>"
			string = string + a[b]['description'] + "</td><td>"
			string = string + "<button type=button value=" + a[b]['id'] + " class='removeLeagueTeam' data-key='{{key}}'>Reject</button><button type=button value=" + a[b]['id'] + " class='editLeagueTeam' data-key='{{key}}'>Accept</button></td></tr>"
		}
		return(string)
	}
	// make an api call and on response render the html page.
	CallApi('leagues/'+req.params['id']).then(function(leagues) {
		CallApi('leagues/'+req.params['id']+'/tournaments').then(function(tournaments) {
			CallApi('leagues/'+req.params['id']+'/teams').then(function(teams) {
				CallApi('leagues/'+req.params['id']+'/teams/requests').then(function(requests) {
					leagues = JSON.parse(leagues)
					res.render('league.html', {
						"title": "League", 
						"user": "Placeholder", 
						"body": leagues, 
						"name": leagues['name'], 
						"owner": leagues['owner_id'], 
						"description": leagues['description'], 
						"entry_fee": leagues['entry_fee'], 
						"tournaments": Card(tournaments),
						"teams": TeamsTable(teams),
						"teams_request": RequestsTable(requests),
						"user": req.session.user, 
						"id": req.session.user_id, 
						"key": req.session.key,
						"files": ['deleteLeague.js', 'deleteLeagueTeam.js', 'editLeagueTeam.js', 'logout.js']
					})
				})
			})
		})
	})
})

// new league
app.get('/leagues/new', function(req, res) {
	res.render('leagueForm.html', {"user": req.session.user, "key": req.session.key, "id": req.session.user_id, "file": "newLeague.js"})
})

// edit league
app.get('/league/:id/edit', function(req, res) {
	res.render('leagueForm.html', {"user": req.session.user, "key": req.session.key, "id": req.session.user_id, "file": "editLeague.js"})
})

// show all teams
app.get('/teams', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('teams').then(function(value){
		team = JSON.parse(value)
		templateVar = resetTempVar()
		templateVar['title'] = 'Teams'
		templateVar['teams'] = team
		res.render('teams.html', templateVar)
	})
})

//show one team
app.get('/team/:id', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('teams/'+req.params['id']).then(function(team){
		CallApi('teams/'+req.params['id']+'/users').then(function(users) {
			team = JSON.parse(team)
			users = JSON.parse(users)
			templateVar = resetTempVar()
			templateVar['title'] = team['name']
			templateVar['name'] = team['name']
			templateVar['description'] = team['description']
			templateVar['users'] = users
			for (var a in users) {
				templateVar['users'][a]['role'] = roles(users[a])
			}
			res.render('team.html', templateVar)
		})
	})
})

// new team
app.get('/teams/new', function(req, res) {
	res.render('teamForm.html', {"user": req.session.user, "key": req.session.key, "id": req.session.user_id, "file": "newTeam.js"})
})

// edit league
app.get('/team/:id/edit', function(req, res) {
	res.render('teamForm.html', {"user": req.session.user,  "key": req.session.key, "id": req.session.user_id, "file": "editTeam.js"})
})

app.get('/tournaments', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('tournaments').then(function(value) {
		templateVar = resetTempVar()
		templateVar['title'] = 'Tournaments'
		templateVar['tournaments'] = JSON.parse(value)
		res.render('tournaments.html', templateVar)	})
})

app.get('/tournament/:id', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('tournaments/'+req.params['id']).then(function(tourn) {
		tourn = JSON.parse(tourn)
		CallApi('tournaments/'+req.params['id']+'/brackets').then(function(brack) {
			templateVar = resetTempVar()
			templateVar['organizer_id'] = tourn['organizer_id']
			templateVar['name'] = tourn['name']
			templateVar['type'] = types(tourn)
			templateVar['size'] = tourn['size']
			templateVar['start_date'] = tourn['start_date']
			templateVar['end_date'] = tourn['end_date']
			templateVar['entry_fee'] = tourn['entry_fee']
			templateVar['description'] = tourn['description']
			templateVar['brack'] = JSON.parse(brack)
			res.render('tournament.html', templateVar)	
		})
	})
})

app.listen(port)