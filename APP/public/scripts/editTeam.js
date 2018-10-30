$(document).ready(function() {
  $("#teamForm").submit(function(event) {
    var form = $(this);
    event.preventDefault();
    id = window.location.pathname.split('/')[2]
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/teams/" + id,
      data: form.serialize(), // serializes the form's elements.
      success: function() {
        window.location.replace("/teams");
      },
      error: function() {
        window.location.replace("/teams");
      }
    });
  });
});