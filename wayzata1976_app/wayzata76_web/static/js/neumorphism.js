
$(document).ready(function() {


    $('.tab').hide();
    $('.tab-header').hide();
    $('.tab-music').show();
    $('.music-header').show();
    $('.youtube-player').hide();




    $('.btn-neumo').click(function() {
        let hasActive = $(this).hasClass('active');
        $('.btn').removeClass('active');
        if (!hasActive) {
            $(this).addClass('active');
        }
        $('.tab').hide();
        $('.tab-header').hide();
        $('.sports-header .academy-header .movie-header .tv-header .music-header').hide();
        $($(this).data('activate')).show();
        $($(this).data('header')).show();
    });



    $(window).scroll(function() {
        if ($(this).scrollTop() > 780) {
          $('th.music-th').css('color', 'rgba(235,235,235,0.8)');
        } else {
          $('th.music-th').css('color', 'rgba(136, 165, 191, 0.48)');
        }
    });



    $(window).scroll(function() {
        if ($(this).scrollTop() > 500) {
          $('#scroll').fadeIn();
        } else {
          $('#scroll').fadeOut();
        }
    });




    $('#scroll').click(function() {
        $('#scroll').tooltip('hide');
        $('html, body').animate({ scrollTop: 0 }, 350);
        return false;
    });

  

    $('#scroll').on('tap', () => {
        $('#scroll').tooltip('hide');
        $('html, body').animate({ scrollTop: 0}, 350);
        return false;
    });


    // $('#scroll').tooltip.show();


    $('tbody tr td, tbody tr th').hover(
        function() {
            $(this).parent().children().css('background-color', '#292b2c');
        }, function() {
            $(this).parent().children().css('background-color', 'initial');
        }
    );

    $('tbody tr.song-row td, tbody tr.song-row th').click(function() {
        let player = $($(this).parent().data('player'));
        let visible = player.is(':visible');
        $('.youtube-player').hide();
        if (!visible) {
            player.show();
        }
    });

});


