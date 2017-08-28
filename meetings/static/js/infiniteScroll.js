$(document).ready(function () {
  $(window).scrollTop(0);
  var numPage = 2;
  $(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() >= ($(document).height())) {
      getData(numPage);
      numPage ++;
    }
  });
});

$(document).ready(function (){
  $('.popWindow').click(function () {
    popClick(this.id)
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
      success: function(response){

        response = $(response);
        masonryItems = response.filter('.masonryItem');

        [].forEach.call(masonryItems, function (masonryItem) {
          var grid = document.querySelector('.masonry');
          var item = document.createElement('div');
          var h = masonryItem.outerHTML;

          salvattore['append_elements'](grid, [item]);
          item.outerHTML = h;

          var $newElem = $('.newItem');
          $newElem.on('click', function () {
            popClick(this.id)
          });
          $newElem.removeClass('newItem')

        });
      }
  });
}

function like(event) {
  const eventMemberId = event.data.eventMemberId;
  const eventId = event.data.eventId;
  $.ajax({
    type: "POST",
    url: $('meta[name="_rateUser"]').attr('content'),
    data: {
      'value': 1,
      'eventMemberId': eventMemberId,
      'eventId': eventId,
      'csrfmiddlewaretoken': $('meta[name="_token"]').attr('content'),
      success: function(){
        $('#likeButton').parent().removeClass('like').addClass('likeActive');
        $('#dislikeButton').parent().removeClass('dislikeActive').addClass('dislike');

        $('#'+eventMemberId).find('img.itemImage').addClass('visited')

      }
    }
  });
}

function dislike(event) {
  const eventMemberId = event.data.eventMemberId;
  const eventId = event.data.eventId;
  $.ajax({
    type: "POST",
    url: $('meta[name="_rateUser"]').attr('content'),
    data: {
      'value': 0,
      'eventMemberId': eventMemberId,
      'eventId': eventId,
      'csrfmiddlewaretoken': $('meta[name="_token"]').attr('content'),
      success: function(){
        $('#dislikeButton').parent().removeClass('dislike').addClass('dislikeActive');
        $('#likeButton').parent().removeClass('likeActive').addClass('like');

        $('div#'+eventMemberId).find('img.itemImage').addClass('visited')

      }
    }
  });
}

function popClick(eventMemberId) {
  $.ajax({
    type: 'GET',
    url: $('meta[name="_getMemberInfo"]').attr('content'),
    data: {eventMemberId: eventMemberId},
    success: function(response) {

      const $elem = $('div#' + eventMemberId).children('div#eventMemberData');
      const firstName = $elem.data('firstName');
      const lastName = $elem.data('lastName');
      const userImage = $elem.data('image');

      const onlineStatus = response.userData.onlineStatus;
      const event = response.eventData.eventName;
      const eventId = response.eventData.eventId;

      $('#userName').html(firstName + ' ' + lastName);
      $('#userOnline').html(onlineStatus);
      $('#userImage').attr('src', userImage);
      $('#userLink').attr('href', 'https://vk.com/id'+eventMemberId);
      $('#event').html(event);

      var $dislikeButton = $('#dislikeButton');
      var $likeButton = $('#likeButton');

      $dislikeButton.parent().removeClass('dislikeActive');
      $likeButton.parent().removeClass('likeActive');

      if (response.choice){
        $likeButton.parent().addClass('likeActive');
      } else if (response.choice == false) {
        $dislikeButton.parent().addClass('dislikeActive');
      }

      $likeButton.off('click').on('click', { eventMemberId: eventMemberId, eventId: eventId }, like);
      $dislikeButton.off('click').on('click', { eventMemberId: eventMemberId, eventId: eventId }, dislike);
    }
  });
}
