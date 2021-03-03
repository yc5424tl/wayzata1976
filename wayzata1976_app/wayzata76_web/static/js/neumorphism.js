
$(document).ready(function() {

    $('.tab').hide();
    $('.tab-header').hide();
    $('.tab-music').show();
    $('.music-header').show();

    $('.btn-neumo').click(function() {
        let hasActive = $(this).hasClass('active');
        $('.btn').removeClass('active');
        if (!hasActive) {
            $(this).addClass('active');
        };
        $('.tab').hide();
        $('.tab-header').hide();
        $('.sports-header .academy-header .movie-header .tv-header .music-header').hide();
        $($(this).data('activate')).show();
        $($(this).data('header')).show();
        // $($(this).data('header')).show();
        // if ($(this).data('activate') === '.tab-music') {
        //   $('.music-header').show();
        // };
        // if ($(this).data('activate') === '.tab-academy') {
        //   $('.academy-header').show();
        // };
        // if ($(this).data('activate') === '.tab-sports') {
        //   $('.sports-header').show();
        // };
        // if ($(this).data('activate') === '.tab-movie') {
        //   $('.movie-header').show();
        // };
        // if ($(this).data('activate') === '.tab-tv') {
        //   $('.tv-header').show();
        // };
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
  
      $('#scroll').tooltip('show');

});


