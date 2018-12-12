$(document).ready(function() {
  $(".deleteTeam").click(function(event) {
    event.preventDefault();
    $.ajax({
      type: "DELETE",
      url: "http://localhost:5000/teams/" + $(this).data('id'),
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.replace('/teams');
      },
      error: function() {
        alert('error');
      }
    });
  })
})