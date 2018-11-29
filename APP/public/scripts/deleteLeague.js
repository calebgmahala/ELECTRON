$(document).ready(function() {
  $("#deleteLeague").click(function(event) {
  console.log(this)
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/leagues/" + id,
    headers: {"request_key": $(this).data('key') },
    success: function() {
      window.location.replace("/leagues");
    },
    error: function() {
      window.location.replace("/leagues");
    }
  });
})
})