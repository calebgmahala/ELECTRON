var request = require("request");
var sinon = require("sinon")
var base_url = "http://localhost:5000/"

beforeEach(function() {
    this.xhr = sinon.useFakeXMLHttpRequest();
    var requests = this.requests = [];

    this.xhr.onCreate = function (xhr) {
        requests.push(xhr);
    };
});

afterEach(function() {
    this.xhr.restore();
});

describe("Leagues", function() {
  it("newLeague", function() {
  	var spy = sinon.spy
  	document.location="http://localhost:3000/leagues/new"
  	document.getElementById('name').value('Test')
  	document.getElementById('entry_fee').value('1234')
  	document.getElementById('description').value('Test')
  	document.getElementById('leagueForm').submit()
  	this.requests[0].setStatus(200)
  	console.log(spy)
    // expect(true).toBe(true);
  });

  it("editLeague", function() {
    expect(true).toBe(true);
  });

  it("deleteLeague", function() {
    expect(true).toBe(true);
  });
});