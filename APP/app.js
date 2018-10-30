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
function CallApi(a, b) {
	request('http://localhost:5000/'+a, function (error, response, body) {
    	if (!error && response.statusCode == 200) {	
    		b(body)// callback function passed from route
  		} else {
  			return('fail')
  		}
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
	CallApi('leagues', function(body){
		res.render('leagues.html', {"table": Table(body), "title": "Leagues", "user": "Placeholder", "body": body})
	})
})

// show one leagues
app.get('/league/:id', function(req, res) {
	// make an api call and on response render the html page.
	CallApi('leagues/'+req.params['id'], function(body){
		tbody = JSON.parse(body)
		res.render('league.html', {"title": "League", "user": "Placeholder", "body": body, "name": tbody['name'], "owner": tbody['owner_id'], "description": tbody['description'], "entry_fee": tbody['entry_fee'], "file": "deleteLeague.js"})
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
	CallApi('teams', function(body){
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