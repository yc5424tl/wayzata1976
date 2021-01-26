$(document).ready(function() {

 

    $(document).on('click', '.allow-focus #nav-pics-dropdown', function (e) {
        e.stopPropagation();
      });

      // Collapse accordion every time dropdown is shown
    $('.dropdown-accordion').on('show.bs.dropdown', function (event) {
      var accordion = $(this).find($(this).data('accordion'));
      accordion.find('.panel-collapse.in').collapse('hide');
    });

    // Prevent dropdown to be closed when we click on an accordion link
    $('.dropdown-accordion').on('click', 'a[data-toggle="collapse"]', function (event) {
      event.preventDefault();
      event.stopPropagation();
      $($(this).data('parent')).find('.panel-collapse.in').collapse('hide');
      $($(this).attr('href')).collapse('show');
    });
});