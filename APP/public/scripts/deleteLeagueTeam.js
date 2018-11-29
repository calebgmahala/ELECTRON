$(document).ready(function() {
  $(".removeLeagueTeam").click(function(event) {
  console.log(this)
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "DELETE",
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