$(document).ready(function() {
  $("#logout").click(function(event) {
    event.preventDefault();
    $.ajax({
      type: "GET",
      url: "http://localhost:3000/logout",
      success: function(data) {
        window.location.replace("/login");
      },
      error: function() {
        alert('error during login')
      }
    });
  });
});