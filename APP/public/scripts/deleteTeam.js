function removeTeam() {
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/teams/" + id,
    headers: {"request_key": $(this).data('key') },
    success: function() {
      window.location.replace("/teams");
    },
    error: function() {
      window.location.replace("/teams");
    }
  });
}