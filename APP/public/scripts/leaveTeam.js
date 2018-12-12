$(document).ready(function() {
  $("#leaveTeam").click(function(event) {
    event.preventDefault();
    id = window.location.pathname.split('/')[2]
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/users/" + id,
      data: {"team_id": 'none'},
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.reload();
      },
      error: function(err) {
        alert(err);
      }
    });
  })
})