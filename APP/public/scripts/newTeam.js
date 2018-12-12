$(document).ready(function() {
  $("#teamForm").submit(function(event) {
    event.preventDefault();
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/teams",
      data: $(this).serialize(), // serializes the form's elements.
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.replace("/teams");
      },
      error: function() {
        alert('error');
      }
    });
  });
});