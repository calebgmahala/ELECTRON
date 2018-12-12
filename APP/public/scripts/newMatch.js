$(document).ready(function() {
  $("#matchForm").submit(function(event) {
    id = window.location.pathname.split('/')[2]
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/tournaments/" + id + "/matches",
      data: $(this).serialize(), // serializes the form's elements.
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.replace("/matches/"+id);
      },
      error: function() {
        alert('error');
      }
    });
  });
});