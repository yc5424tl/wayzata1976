$(document).ready(function() {

    $('.table-view-select').on('change', function() {
        $('.toggle-hidden').hide();
        let selection = (this.value);
        $(this.value).show();
    });

    $('.mia_list').hide();
    $('.passed_list').hide();
    $('.in_contact_list').hide();


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

    // https://stackoverflow.com/a/50097818/15027952
    $('a.scrollLink').click(function(event) {
      event.preventDefault();
      $('html, body').animate({
        scrollTop: $($(this).attr('href')).offset().top
      }, 500);
    });

    $('a.scrollLink').on('tap', function(event) {
      event.preventDefault();
      $('html, body').animate({ scrollTop: $($(this).attr('href')).offset().top
      }, 500);
    });

});