$(document).ready(function() {
  $("#joinLeague").click(function(event) {
    event.preventDefault();
    id = window.location.pathname.split('/')[2]
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/leagues/" + id + "/teams",
      data: {"organizer_id": id, 'team_id': $(this).data('team_id')},
      headers: {"request_key": $(this).data('key')},
      success: function() {
        window.location.reload();
      },
      error: function(xhr, status, error) {
        alert('error')
      }
    });
  })
})