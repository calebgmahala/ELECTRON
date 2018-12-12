$(document).ready(function() {
  $("#matchForm").submit(function(event) {
    $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
    id = window.location.pathname.split('/')[4]
    event.preventDefault();
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/matches/"+id,
      data: $(this).serialize(), // serializes the form's elements.
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.replace("/matches/"+id);
      },
      error: function() {
        alert('error');
      }
    });
  });
});