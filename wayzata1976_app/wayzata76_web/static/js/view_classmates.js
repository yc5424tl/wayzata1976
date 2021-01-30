$(document).ready(function() {

    $('.table-view-select').on('change', function() {
        $('.toggle-hidden').hide();
        let selection = (this.value);
        $(this.value).show()
    });

    $('.mia_list').hide();
    $('.passed_list').hide();
    $('.in_contact_list').hide();


    $(window).scroll(function() {
      if ($(this).scrollTop() > 100) {
        $('#scroll').fadeIn();
      } else {
        $('#scroll').fadeIn();
      }
    })

    $('#scroll').click(function() {
      $('html', 'body').animate({ scrollTop: 0 }, 600);
      return false;    
    })


});