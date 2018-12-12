$(document).ready(function() {
  $(".removeLeagueTeam").click(function(event) {
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/leagues/" + id + "/teams/" + $(this).data('id'),
    headers: {"request_key": $(this).data('key') },
    success: function() {
      window.location.replace("/league/"+id);
    },
    error: function() {
      alert('error');
    }
  });
  })
})