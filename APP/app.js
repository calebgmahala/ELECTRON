// express is main framework
const express = require('express')
const app = express()
const port = 3000

// require is used to send out api requests
const request = require('request')

// mustache is template handler
var mustache = require('mustache-express');
app.engine('html', mustache());
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
	CallApi('leagues', function(body){
		res.render('leagues.html', {"body": body})
	})
})

app.listen(port)