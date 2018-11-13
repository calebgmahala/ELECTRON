$(document).ready(function() {
  $("#loginForm").submit(function(event) {
    var form = $(this);
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/users",
      data: form.serialize(), // serializes the form's elements.
      success: function() {
        window.location.replace("/users");
      },
      error: function() {
        window.location.replace("/users");
      }
    });
  });
});