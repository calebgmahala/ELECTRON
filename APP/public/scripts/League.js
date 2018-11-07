$(document).ready(function() {
  $(".editLeagueTeam").click(function(event) {
  console.log(this)
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "PUT",
    data: {"request": 0},
    url: "http://localhost:5000/leagues/" + id + "/teams/" + this.value,
    success: function() {
      window.location.replace("/league/"+id);
    },
    error: function() {
      window.location.replace("/league/"+id);
    }
  });
  })
})

$(document).ready(function() {
  $(".removeLeagueTeam").click(function(event) {
  console.log(this)
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/leagues/" + id + "/teams/" + this.value,
    success: function() {
      window.location.replace("/league/"+id);
    },
    error: function() {
      window.location.replace("/league/"+id);
    }
  });
  })
})

function removeLeague() {
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/leagues/" + id,
    success: function() {
      window.location.replace("/leagues");
    },
    error: function() {
      window.location.replace("/leagues");
    }
  });
}