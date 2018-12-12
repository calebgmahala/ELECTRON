$(document).ready(function() {
  $(".deleteUser").click(function(event) {
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/users/" + $(this).data('id'),
    headers: {"request_key": $(this).data('key') },
    success: function() {
      window.location.replace("/users");
    },
    error: function() {
      alert('error')
    }
  });
})
})