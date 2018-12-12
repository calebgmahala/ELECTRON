$(document).ready(function() {
  $(".deleteLeague").click(function(event) {
  event.preventDefault();
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/leagues/" + $(this).data('id'),
    headers: {"request_key": $(this).data('key') },
    success: function() {
      window.location.replace("/leagues");
    },
    error: function() {
      alert('error');
    }
  });
})
})