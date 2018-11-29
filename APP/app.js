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
			res.sendStatus(200) 
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
			res.sendStatus(200) 
  		} else {
  			res.sendStatus(404)
  		}
	});
})

app.get('/signup', function(req, res) {
	templateVar['file'] = 'signup.js'
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

app.get('/user/:id', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('users/'+req.params['id']).then(function(user) {
		user = JSON.parse(user)
		CallApi('teams/'+user['team_id']).then(function(team) {
			team = JSON.parse(team)
			templateVar = resetTempVar()
			templateVar['title'] = 'Profile'
			templateVar['username'] = user['username']
			templateVar['team_id'] = user['team_id']
			templateVar['team_name'] = team['name']
			templateVar['description'] = user['description']
			templateVar['role'] = roles(user)
			res.render('user.html', templateVar)
		})
	})
})
// show all leagues
app.get('/leagues', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('leagues').then(function(value) {
		templateVar = resetTempVar()
		templateVar['title'] = 'Leagues'
		templateVar['leagues'] = JSON.parse(value)
		res.render('leagues.html', templateVar)	})
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
			string = string + "<button type=button value=" + a[b]['id'] + " class='removeLeagueTeam'>Kick</button></td></tr>"
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
			string = string + "<button type=button value=" + a[b]['id'] + " class='removeLeagueTeam'>Reject</button><button type=button value=" + a[b]['id'] + " class='editLeagueTeam'>Accept</button></td></tr>"
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
						"key": req.session.key
					})
				})
			})
		})
	})
})

// new league
app.get('/leagues/new', function(req, res) {
	res.render('leagueForm.html', {"user": req.session.user, "file": "newLeague.js"})
})

// edit league
app.get('/league/:id/edit', function(req, res) {
	res.render('leagueForm.html', {"user": req.session.user, "file": "editLeague.js"})
})

// show all teams
app.get('/teams', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('teams').then(function(value){
		templateVar = resetTempVar()
		templateVar['title'] = 'Teams'
		templateVar['teams'] = JSON.parse(value)
		res.render('teams.html', templateVar)
	})
})

//show one team
app.get('/team/:id', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('teams/'+req.params['id']).then(function(team){
		team = JSON.parse(team)
		templateVar = resetTempVar()
		templateVar['name'] = team['name']
		templateVar['description'] = team['description']
		res.render('team.html', templateVar)
	})
})

// new team
app.get('/teams/new', function(req, res) {
	res.render('teamForm.html', {"user": req.session.user, "file": "newTeam.js"})
})

// edit league
app.get('/team/:id/edit', function(req, res) {
	res.render('teamForm.html', {"user": req.session.user, "file": "editTeam.js"})
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