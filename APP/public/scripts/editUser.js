$(document).ready(function() {
  $("#userForm").submit(function(event) {
    $(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
    event.preventDefault();
    id = window.location.pathname.split('/')[2]
    $.ajax({
      type: "PUT",
      url: "http://localhost:5000/users/" + id,
      data: $(this).serialize(), // serializes the form's elements.
      headers: {"request_key": $(this).data('key') },
      success: function() {
        window.location.replace("/user/" + id);
      },
      error: function() {
        window.location.reload();
      }
    });
  });
});