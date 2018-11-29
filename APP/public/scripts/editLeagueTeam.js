$(document).ready(function() {
  $(".editLeagueTeam").click(function(event) {
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "PUT",
    data: {"request": 0},
    url: "http://localhost:5000/leagues/" + id + "/teams/" + this.value,
    headers: {"request_key": $(this).data('key') },
    success: function() {
      window.location.replace("/league/"+id);
    },
    error: function() {
      window.location.replace("/league/"+id);
    }
  });
  })
})