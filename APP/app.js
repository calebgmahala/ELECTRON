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

//templateVar is used to build out variables passed to templates
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

// this function resets templateVar back to the bare bone variables. (session)
function resetTempVar() {
	var resp = {}
	resp['user'] = templateVar["user"]
	resp['id'] = templateVar["id"]
	resp['key'] = templateVar["key"]
	resp['perms'] = templateVar["perms"]
	resp['owner_team_id'] = templateVar['owner_team_id']

	return resp
}

// change number roles to words
function roles(user) {
	if (user['role'] == 1) {
		return 'rifler'
	} else if (user['role'] == 2) {
		return 'awper'
	} else{
		return 'undefined'
	}
}

// change league types to words
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
			CallApi('users/'+body['id']).then(function(user){
				user = JSON.parse(user)
				if (user['is_owner_team'] == 1) {
					req.session.owner_team_id = user['team_id']
					templateVar['owner_team_id'] = user['team_id']
				}
	    		req.session.user = body['username']
	    		req.session.user_id = body['id']
	    		req.session.key = body['request_key']
	    		req.session.perms = body['permission']
	    		//sets templatevar for later use anyware in the file
	    		templateVar["user"] = body['username']
	    		templateVar["id"] = body['id']
	    		templateVar["key"] = body['request_key']
	    		templateVar["perms"] = body['permission']
				res.status(200)
				res.send(body['id'].toString())
			})
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

// get all users
app.get('/users', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('users').then(function(users) {
		users = JSON.parse(users)
		templateVar = resetTempVar()
		templateVar['title'] = 'Users'
		templateVar['users'] = users
		templateVar['files'] = ['logout.js', 'deleteUser.js']
		if (templateVar['perms'] == 2) {
			templateVar['admin'] = 1
		}
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

// get one user
app.get('/user/:id', async function(req, res) {
	var promiseArray = []
	var resp = {}
	// response varables set here so they can 
	// be appended to in the promise nesting
	// and called later on in the endpoint

	// promises are nested due to api endpoints 
	// not giveing relative data
	resp['user'] = []
	resp['team'] = []
	resp['leagues'] = []
	// make an api call and on response render the html page.
	var prom0 = CallApi('users/'+req.params['id'])
	promiseArray.push(prom0) // promise is added to array that will be used at end of endpoint
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
		//checks for self
		if (resp['user']['id'] == templateVar['id']) {
			templateVar['self'] = true;
		}
		if (templateVar['perms'] == 2) {
			templateVar['admin'] = true;
		}
		templateVar["files"] = ['logout.js', 'leaveTeam.js', 'deleteUser.js']
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
		//builds out stats
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

// edit user
app.get('/user/:id/edit', async function(req, res) {
	CallApi('users/'+req.params['id']).then(function(user) {
		user = JSON.parse(user)
		templateVar = resetTempVar()
		templateVar['files'] = ['editUser.js']
		templateVar['title'] = 'Edit Profile'
		templateVar['description'] = user['description']
		if (templateVar['perms'] == 2) {
			templateVar['admin'] = 1
		}
		res.render('userForm.html', templateVar)
	})
})

// show all leagues
app.get('/leagues', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('leagues').then(function(value) {
		templateVar = resetTempVar()
		templateVar['title'] = 'Leagues'
		templateVar['leagues'] = JSON.parse(value)
		templateVar['files'] = ['logout.js', 'deleteLeague.js']
		if (templateVar['perms'] == 2) {
			templateVar['admin'] = 1
		}
		if (templateVar['perms'] == 2 || templateVar['perms'] == 1) {
			templateVar['new'] = 1
		}
		res.render('leagues.html', templateVar)
	})
})

// show one leagues
app.get('/league/:id', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('leagues/'+req.params['id']).then(function(leagues) {
		CallApi('leagues/'+req.params['id']+'/tournaments').then(function(tournaments) {
			CallApi('leagues/'+req.params['id']+'/teams').then(function(teams) {
				CallApi('leagues/'+req.params['id']+'/teams/requests').then(function(requests) {
					leagues = JSON.parse(leagues)
					tournaments = JSON.parse(tournaments)
					teams = JSON.parse(teams)
					requests = JSON.parse(requests)
					templateVar = resetTempVar()
					if (leagues['owner_id'] == templateVar['id']) {
						templateVar['self'] = true;
					}
					templateVar["title"] = "League"
					templateVar["name"] = leagues['name']
					templateVar["owner"] = leagues['owner_id']
					templateVar["description"] = leagues['description']
					templateVar["entry_fee"] = leagues['entry_fee']
					templateVar['league_id'] = leagues['id']
					templateVar["tournaments"] = tournaments
					templateVar["teams"] = teams
					templateVar["teams_requests"] = requests
					templateVar["files"] = ['deleteLeague.js', 'deleteLeagueTeam.js', 'editLeagueTeam.js', 'logout.js', 'joinLeague.js']
					res.render('league.html', templateVar)
				})
			})
		})
	})
})

// new league
app.get('/leagues/new', function(req, res) {
	templateVar = resetTempVar()
	templateVar['files'] = ['newLeague.js']
	res.render('leagueForm.html', templateVar)
})

// edit league
app.get('/league/:id/edit', function(req, res) {
	templateVar = resetTempVar()
	templateVar['files'] = ['editLeague.js']
	if (templateVar['perms'] == 2) {
			templateVar['admin'] = 1
	}
	templateVar['files'] = ['logout.js', 'deleteTeam.js']
	res.render('leagueForm.html', templateVar)
})

// show all teams
app.get('/teams', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('teams').then(function(value){
		team = JSON.parse(value)
		templateVar = resetTempVar()
		if (templateVar['perms'] == 2) {
				templateVar['admin'] = 1
		}
		templateVar['title'] = 'Teams'
		templateVar['teams'] = team
		templateVar["files"] = ['logout.js','deleteTeam.js']
		res.render('teams.html', templateVar)
	})
})

//show one team
app.get('/team/:id', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('teams/'+req.params['id']).then(function(team){
		CallApi('teams/'+req.params['id']+'/users').then(function(users) {
			CallApi('teams/'+req.params['id']+'/leagues').then(function(leagues) {
				team = JSON.parse(team)
				users = JSON.parse(users)
				leagues = JSON.parse(leagues)
				templateVar = resetTempVar()
				if (templateVar['owner_team_id'] == req.params['id']) {
					templateVar['owner'] = 1
				}
				templateVar['tid'] = req.params['id']
				templateVar['title'] = team['name']
				templateVar['tname'] = team['name']
				templateVar['description'] = team['description']
				templateVar['users'] = users
				templateVar['leagues'] = leagues
				templateVar["files"] = ['logout.js','deleteTeam.js']
				for (var a in users) {
					templateVar['users'][a]['role'] = roles(users[a])
				}
				res.render('team.html', templateVar)
			})
		})
	})
})

// new team
app.get('/teams/new', function(req, res) {
	res.render('teamForm.html', {"user": req.session.user, "key": req.session.key, "id": req.session.user_id, "file": "newTeam.js"})
})

// edit team
app.get('/team/:id/edit', function(req, res) {
	templateVar = resetTempVar()
	templateVar['files'] = ['editTeam.js']
	if (templateVar['owner_team_id'] == req.params['id']) {
		templateVar['self'] = 1
	}
	res.render('teamForm.html', templateVar)
})

// join team
app.get('/team/:id/join', async function(req, res) {
	templateVar = resetTempVar()
	templateVar["files"] = ['joinTeam.js']
	templateVar['title'] = 'Join Team'
	res.render('joinTeam.html', templateVar)
})

// get all tournaments
app.get('/tournaments', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('tournaments').then(function(value) {
		templateVar = resetTempVar()
		templateVar['title'] = 'Tournaments'
		templateVar['tournaments'] = JSON.parse(value)
		for (var a in templateVar['tournaments']) {
			templateVar['tournaments'][a]['type'] = types(templateVar['tournaments'][a])
		}
		res.render('tournaments.html', templateVar)	})
})

// get one tournament
app.get('/tournament/:id', async function(req, res) {
	var promiseArray = []
	var resp = {}
	resp['matches'] = []
	resp['tourn'] = {}
	resp['brack'] = []
	// make an api call and on response render the html page.
	var prom0 = CallApi('tournaments/'+req.params['id'])
	promiseArray.push(prom0)
	await prom0.then(async function(tourn) {
		tourn = JSON.parse(tourn)
		resp['tourn'] = tourn
		var prom1 = CallApi('tournaments/'+req.params['id']+'/brackets')
		promiseArray.push(prom1)
		await prom1.then(async function(brack) {
			brack = JSON.parse(brack)
			resp['brack'] = brack
			for (var b in brack) {
				var prom5 = CallApi('teams/'+brack[b]['team_id'])
				promiseArray.push(prom5)
				await prom5.then(async function(team) {
					team = JSON.parse(team)
					brack[b]['team'] = team['name']
					resp['brack'] = brack
				})
			}
			var prom2 = CallApi('tournaments/'+req.params['id']+'/matches')
			promiseArray.push(prom2)
			await prom2.then(async function(matches) {
				matches = JSON.parse(matches)
				resp['matches'] = matches
				for (var a in matches) {
					var prom3 = CallApi('teams/'+matches[a]['home_id'])
					promiseArray.push(prom3)
					await prom3.then(async function(hteam) {
						var prom4 = CallApi('teams/'+matches[a]['away_id'])
						promiseArray.push(prom4)
						await prom4.then(async function(ateam) {
							hteam = JSON.parse(hteam)
							ateam = JSON.parse(ateam)
							matches[a]['hteam'] = hteam['name']
							matches[a]['ateam'] = ateam['name']
							resp['matches'] = matches
							resp['tourn'] = tourn
							resp['brack'] = brack
						})
					})
				}
			})
		})
	})
	await Promise.all(promiseArray).then(async function(value) {
		templateVar = resetTempVar()
		CallApi('leagues/'+resp['tourn']['organizer_id']).then(function(org) {
			org = JSON.parse(org)
			if (templateVar['id'] == org['owner_id']) {
				templateVar['owner'] = 1
			}
			templateVar['organizer_id'] = resp['tourn']['organizer_id']
			templateVar['tid'] = resp['tourn']['id']
			templateVar['title'] = resp['tourn']['name']
			templateVar['name'] = resp['tourn']['name']
			templateVar['type'] = types(resp['tourn'])
			templateVar['size'] = resp['tourn']['size']
			templateVar['start_date'] = resp['tourn']['start_date']
			templateVar['end_date'] = resp['tourn']['end_date']
			templateVar['entry_fee'] = resp['tourn']['entry_fee']
			templateVar['description'] = resp['tourn']['description']
			templateVar['brack'] = resp['brack']
			templateVar['matches'] = resp['matches']
			templateVar['files'] = ['logout.js', 'deleteMatch.js']
			res.render('tournament.html', templateVar)
		})
	})
})

// get one match
app.get('/matches/:id', async function(req, res) {
	var promiseArray = []
	var resp = {}
	resp['match'] = {}
	resp['lead'] = []
	var prom0 = CallApi('matches/'+req.params['id'])
	promiseArray.push(prom0)
	// make an api call and on response render the html page.
	await prom0.then(async function(match) {
		var prom1 = CallApi('matches/'+req.params['id']+'/leaderboard')
		promiseArray.push(prom1)
		await prom1.then(async function(lead) {
			match = JSON.parse(match)
			lead = JSON.parse(lead)
			var prom2 = CallApi('teams/'+match['home_id'])
			promiseArray.push(prom2)
			await prom2.then(async function(hteam) {
				hteam = JSON.parse(hteam)
				match['hteam'] = hteam
				resp['match'] = match
				var prom3 = CallApi('teams/'+match['away_id'])
				promiseArray.push(prom3)
				await prom3.then(async function(ateam) {
					ateam = JSON.parse(ateam)
					match['ateam'] = ateam
					resp['match'] = match
					for (var a in lead) {
						if (lead[a]['team_id'] == match['home_id']) {
							lead[a]['home'] = true
						} else {
							lead[a]['away'] = true
						}
						var prom4 = CallApi('users/'+lead[a]['player_id'])
						promiseArray.push(prom4)
						await prom4.then(async function(user) {
							user = JSON.parse(user)
							lead[a]['user'] = user
							resp['match'] = match
							resp['lead'] = lead
						})
					}
				})
			})
		})
	})
	await Promise.all(promiseArray).then(async function(value) {
		templateVar = resetTempVar()
		templateVar['tournament_id'] = resp['match']['tournament_id']
		templateVar['home_id'] = resp['match']['home_id']
		templateVar['away_id'] = resp['match']['away_id']
		templateVar['home_score'] = resp['match']['home_score']
		templateVar['away_score'] = resp['match']['away_score']
		templateVar['start_date'] = resp['match']['start_date']
		templateVar['end_date'] = resp['match']['end_date']
		templateVar['match'] = resp['match']
		templateVar['leaderboard'] = resp['lead']
		templateVar['files'] = ['logout.js']
		res.render('matches.html', templateVar)
	})
})

// new match
app.get('/tournament/:id/matches/new', function(req, res) {
	CallApi('tournaments/'+req.params['id']).then(function(tourn) {
		tourn = JSON.parse(tourn)
		CallApi('leagues/'+tourn['organizer_id']+'/teams').then(function(teams) {
			teams = JSON.parse(teams)
			if (templateVar['perms'] == 2) {
				templateVar['admin'] = 1
			}
			templateVar['teams'] = teams
			templateVar['files'] = ['newMatch.js']
			templateVar['new'] = 1
			res.render('matchForm.html', templateVar)
		})
	})
})

// edit match
app.get('/tournament/:t_id/matches/:id/edit', function(req, res) {
	CallApi('tournaments/'+req.params['t_id']).then(function(tourn) {
		tourn = JSON.parse(tourn)
		CallApi('leagues/'+tourn['organizer_id']+'/teams').then(function(teams) {
			teams = JSON.parse(teams)
			if (templateVar['perms'] == 2) {
				templateVar['admin'] = 1
			}
			templateVar['teams'] = teams
			templateVar['files'] = ['editMatch.js']
			res.render('matchForm.html', templateVar)
		})
	})
})

app.listen(port)