$(document).ready(function() {
  $("#teamForm").submit(function(event) {
    $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
    event.preventDefault();
    id = window.location.pathname.split('/')[2]
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/teams/" + id,
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