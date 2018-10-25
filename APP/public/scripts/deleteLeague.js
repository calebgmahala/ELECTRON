function remove() {
  id = window.location.pathname.split('/')[2]
  $.ajax({
    type: "DELETE",
    url: "http://localhost:5000/leagues/" + id,
    success: function() {
      window.location.replace("/leagues");
    },
    error: function() {
      window.location.replace("/leagues");
    }
  });
}