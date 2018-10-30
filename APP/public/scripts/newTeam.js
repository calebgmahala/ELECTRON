$(document).ready(function() {
  $("#teamForm").submit(function(event) {
    var form = $(this);
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/teams",
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