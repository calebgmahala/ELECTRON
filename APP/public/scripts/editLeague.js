$(document).ready(function() {
  $("#leagueForm").submit(function(event) {
    event.preventDefault();
    $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
    id = window.location.pathname.split('/')[2]
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/leagues/" + id,
      data: $(this).serialize(), // serializes the form's elements.
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.replace("/leagues");
      },
      error: function() {
        alert('error');
      }
    });
  });
});