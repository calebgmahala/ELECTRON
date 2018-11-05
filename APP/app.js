// express is main framework
const express = require('express')
const app = express()
app.use(express.static('public'))
const port = 3000

// require is used to send out api requests
const request = require('request')

// mustache is template handler
var mustache = require('mustache-express')
app.engine('html', mustache())
app.set('view engine', 'html')
app.set('views', __dirname + '/views')

//  api request function
function CallApi(a) {
	var resp = ''
	return new Promise(function(resolve, reject){
	    request('http://localhost:5000/'+a, function (error, response, body) {
	    	if (!error && response.statusCode == 200) {	
	    		resolve(body)// callback function passed from route
	  		} else {
	  			reject(Error(error + " | " + response + " | " + body))
	  		}
		})
	})
}

// show all leagues
app.get('/leagues', function(req, res) {
	// function to put together table for html page
	function Table(a) {
		a = JSON.parse(a)// turn a into object otherwise it is a string
		string = "<tr><th>Id</th><th>Name</th><th>Owner</th><th>Entry Fee</th><th>Description</th></tr>";
		for (var b in a) {
			string = string + "<tr><td>"
			string = string + a[b]['id'] + "</td><td>"
			string = string + "<a href='/league/" + a[b]['id'] + "'>" + a[b]['name'] + "</a></td><td>"
			string = string + a[b]['owner_id'] + "</td><td>"
			string = string + "$" + a[b]['entry_fee'] + "</td><td>"
			string = string + a[b]['description'] + "</td></tr>"
		}
		return(string)
	}
	// make an api call and on response render the html page.
	CallApi('leagues').then(function(value) {
		res.render('leagues.html', {"table": Table(value), "title": "Leagues", "user": "Placeholder", "body": value})
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
			string = string + "<a href='/teams/" + a[b]['id'] + "'>" + a[b]['name'] + "</a></td><td>"
			string = string + a[b]['owner_id'] + "</td><td>"
			string = string + a[b]['description'] + "</td><td>"
			string = string + "<button type=button value=" + a[b]['id'] + " onclick=removeLeagueTeam()>Kick</button></td></tr>"
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
			string = string + "<button type=button value=" + a[b]['id'] + " onclick=removeLeagueTeam()>Reject</button><button type=button value=" + a[b]['id'] + " onclick=editLeagueTeam()>Accept</button></td></tr>"
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
					})
				})
			})
		})
	})
})

// new league
app.get('/leagues/new', function(req, res) {
	res.render('leagueForm.html', {"file": "newLeague.js"})
})

// edit league
app.get('/league/:id/edit', function(req, res) {
	res.render('leagueForm.html', {"file": "editLeague.js"})
})

// show all teams
app.get('/teams', function(req, res) {
	// function to put together table for html page
	function Table(a) {
		a = JSON.parse(a)// turn a into object otherwise it is a string
		string = "<tr><th>Id</th><th>Name</th><th>Owner</th><th>Description</th></tr>";
		for (var b in a) {
			string = string + "<tr><td>"
			string = string + a[b]['id'] + "</td><td>"
			string = string + "<a href='/team/" + a[b]['id'] + "'>" + a[b]['name'] + "</a></td><td>"
			string = string + a[b]['owner_id'] + "</td><td>"
			string = string + a[b]['description'] + "</td></tr>"
		}
		return(string)
	}
	// make an api call and on response render the html page.
	CallApi('teams').then(function(body){
		res.render('leagues.html', {"table": Table(body), "title": "Teams", "user": "Placeholder", "body": body})
	})
})

// show one team
// app.get('/team/:id', function(req, res) {
// 	// make an api call and on response render the html page.
// 	CallApi('teams/'+req.params['id'], function(body){
// 		tbody = JSON.parse(body)
// 		res.render('leagues.html', {"title": "League", "user": "Placeholder", "body": body, "name": tbody['name'], "owner": tbody['owner_id'], "description": tbody['description'], "file": "deleteLeague.js"})
// 	})
// })

// new team
app.get('/teams/new', function(req, res) {
	res.render('teamForm.html', {"file": "newTeam.js"})
})

// edit league
app.get('/team/:id/edit', function(req, res) {
	res.render('teamForm.html', {"file": "editTeam.js"})
})
app.listen(port)