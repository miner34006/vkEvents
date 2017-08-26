$(document).ready(function () {
  $(window).scroll(function() {
    var numPage = 2;
    if ($(window).scrollTop() + $(window).height() >= ($(document).height())) {
      getData(numPage)
    }
  });
});

function getData(numPage) {
  $.ajax({
    type: "GET",
    url: $('meta[name="_infiniteScroll"]').attr('content'),
    dataType: 'html',
    data: {
      'numPage': numPage
    },
      success: function(html){

      }
  });

}