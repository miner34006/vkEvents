$(function() {
  $("input:checkbox").bind("change click", function () {
    response = 0
    if (this.checked) {
      response = 1
    }
    $.ajax({
      type: "POST",
      url: "/changeEventStatus/",
      data: {
        'response': response,
        'eventId': this.getAttribute("id"),
        'csrfmiddlewaretoken': $('meta[name="_token"]').attr('content'),
      }
    });
  });
});


