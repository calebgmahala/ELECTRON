$(document).ready(function() {
  $("#loginForm").submit(function(event) {
    var form = $(this);
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "http://localhost:3000/login",
      data: form.serialize(), // serializes the form's elements.
      success: function(data) {
        window.location.replace("/user/"+data);
      },
      error: function() {
        alert('error during login')
      }
    });
  });
});