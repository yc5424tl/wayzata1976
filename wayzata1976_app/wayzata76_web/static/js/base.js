$(document).ready(function() {

    // Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });

    // make it as accordion for smaller screens
    if ($(window).width() < 992) {
      $('.dropdown-menu a').click(function(e){
        e.preventDefault();
          if($(this).next('.submenu').length){
            $(this).next('.submenu').toggle();
          }
          $('.dropdown').on('hide.bs.dropdown', function () {
        $(this).find('.submenu').hide();
      })
      });
    }



    // window.onclick = function(event) {
    //   if (event.target.matches('.pic-nav')) {
    //     event.stopPropagation();
    //   }
    // }

    // $(document).on('click', '.allow-focus #nav-pics-dropdown', function (e) {
    //     e.stopPropagation();
    //   });

    //   // Collapse accordion every time dropdown is shown
    // $('.dropdown-accordion').on('show.bs.dropdown', function (event) {
    //   var accordion = $(this).find($(this).data('accordion'));
    //   accordion.find('.panel-collapse.in').collapse('hide');
    // });

    // // Prevent dropdown to be closed when we click on an accordion link
    // $('.dropdown-accordion').on('click', 'a[data-toggle="collapse"]', function (event) {
    //   event.preventDefault();
    //   event.stopPropagation();
    //   $($(this).data('parent')).find('.panel-collapse.in').collapse('hide');
    //   $($(this).attr('href')).collapse('show');
    // });
});