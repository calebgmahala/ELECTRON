$(document).ready(function() {
  $("#leagueForm").submit(function(event) {
    var form = $(this);
    event.preventDefault();
    id = window.location.pathname.split('/')[2]
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/leagues/" + id,
      data: form.serialize(), // serializes the form's elements.
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.replace("/leagues");
      },
      error: function() {
        window.location.replace("/leagues");
      }
    });
  });
});