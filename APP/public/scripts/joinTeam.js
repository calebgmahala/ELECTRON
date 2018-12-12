$(document).ready(function() {
  $("#joinForm").submit(function(event) {
    event.preventDefault();
    id = window.location.pathname.split('/')[2]
    uid = $(this).data('id')
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/users/" + uid,
      headers: {"request_key": $(this).data('key'), "team_id": id, "team_key": $('#team_key').val()},
      success: function() {
        window.location.replace("/user/"+uid);
      },
      error: function(xhr, status, error) {
        window.location.replace("/users")
      }
    });
  })
})