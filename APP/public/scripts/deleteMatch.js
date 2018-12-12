$(document).ready(function() {
  $(".deleteMatch").click(function(event) {
  event.preventDefault();
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/matches/" + $(this).data('id'),
    headers: {"request_key": $(this).data('key') },
    success: function() {
      window.location.reload();
    },
    error: function() {
      alert('error');
    }
  });
})
})