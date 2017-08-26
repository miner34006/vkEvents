$(document).ready(function () {
  var numPage = 2;
  $(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() >= ($(document).height()*1)) {
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

          var $newElem = $('.newItem').find('a.popWindow');
          $newElem.on('click', function () {
            popClick(this.id)
          });
          $('.masonryItem').removeClass('newItem')

        });
      }
  });
}

function like(event) {
  const userId = event.data.userId;
  $.ajax({
    type: "POST",
    url: $('meta[name="_rateUser"]').attr('content'),
    data: {
      'value': 1,
      'userId': userId,
      'csrfmiddlewaretoken': $('meta[name="_token"]').attr('content'),
      success: function(){
        $('#likeButton').parent().removeClass('like').addClass('likeActive');
        $('#dislikeButton').parent().removeClass('dislikeActive').addClass('dislike');
        $('#image'+userId).addClass('visited')
      }
    }
  });
}

function dislike(event) {
  const userId = event.data.userId;
  $.ajax({
    type: "POST",
    url: $('meta[name="_rateUser"]').attr('content'),
    data: {
      'value': 0,
      'userId': userId,
      'csrfmiddlewaretoken': $('meta[name="_token"]').attr('content'),
      success: function(){
        $('#dislikeButton').parent().removeClass('dislike').addClass('dislikeActive');
        $('#likeButton').parent().removeClass('likeActive').addClass('like');
        $('#image'+userId).addClass('visited')
      }
    }
  });
}

function popClick(userId) {
  $.ajax({
    type: 'GET',
    url: $('meta[name="_getMemberInfo"]').attr('content'),
    data: {userId: userId},
    success: function(response) {

      const firstName = response.firstName;
      const lastName = response.lastName;
      const userImage = response.image;

      $('#userName').html(firstName + ' ' +lastName);
      $('#userImage').attr('src', userImage);
      $('#userLink').attr('href', 'https://vk.com/id'+userId);

      var $dislikeButton = $('#dislikeButton');
      var $likeButton = $('#likeButton');

      $dislikeButton.parent().removeClass('dislikeActive');
      $likeButton.parent().removeClass('likeActive');

      if (response.choice){
        $likeButton.parent().addClass('likeActive');
      } else if (response.choice == false) {
        $dislikeButton.parent().addClass('dislikeActive');
      }

      $likeButton.off('click').on('click', { userId: userId }, like);
      $dislikeButton.off('click').on('click', { userId: userId }, dislike);
    }
  });
}
