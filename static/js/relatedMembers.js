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

$(document).ready(function (){
  $('.popWindow').click(function () {
    var userId = this.id;
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
  });
});
