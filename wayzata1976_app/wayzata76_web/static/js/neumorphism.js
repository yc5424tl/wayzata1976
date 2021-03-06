
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
        // alert('clicked');
        let player = $($(this).parent().data('player'));
        let visible = player.is(':visible');
        $('.youtube-player').hide();
        if (!visible) {
            player.show();
        }
    });

    // alert('pre-alert');

    // $('tbody tr.song-row td, tbody tr.song-row th').click(function() {
    //     alert('clicked');
    //     $(this).css('color', 'green');
    //     sleep(2000);
    //     if ($('.youtube-player')[0]) {
    //         alert('in 1st if - player exists in this row');
    //         $(this).css('color', 'red');
    //         sleep(2000)
    //         if ( $(this).parent().next().hasClass('youtube-player') ) {
    //             alert('in 2nd if');
    //             $(this).css('color', 'blue');
    //             document.remove('.youtube-player');
    //         } else {
    //             alert('in 1st else - player exists in different row');
    //             $(this).css('color', 'pink');
    //             sleep(2000);
    //             document.remove('.youtube-player');
    //             $(this).parent().after( document.createElement('<tr class="youtube-player"><td colspan="7"><iframe type="text/html" width="100%" height="200" src="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></td></tr>') );
    //             $('.youtube-player').attr('src', $(this).parent().data('url'));

    //             // let url = $($(this).parent().data('url'));
    //             // let player =  document.createElement('<tr class="youtube-player"><td colspan="7"><iframe type="text/html" width="100%" height="200" src="$(url)" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></td></tr>');
    //             // $(this).parent().after(player);
    //             // player.insertAfter($(this).parent())
    //         }
    //     } else {
    //         alert('in 2nd else - no player exists');
    //         $(this).css('color', 'orange');
    //         sleep(2000);
    //         $(this).parent().after( document.createElement('<tr class="youtube-player"><td colspan="7"><iframe type="text/html" width="100%" height="200" src="" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></td></tr>') );
    //         $('.youtube-player').attr('src', $($(this).parent().data('url')));
    //         // let url = $($(this).parent().data('url'));
    //         // let player =  document.createElement('<tr class="youtube-player"><td colspan="7"><iframe type="text/html" width="100%" height="200" src="$(url)" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe></td></tr>');
    //         // $(this).parent().after(player);
    //     }
    // });

    // alert('post-alert');

});


