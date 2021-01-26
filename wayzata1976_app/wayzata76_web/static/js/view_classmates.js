$(document).ready(function() {
    $('.table-view-select').on('change', function() {
        $('.toggle-hidden').hide();
        let selection = (this.value);
        $(this.value).show()
    });

    $('.mia_list').hide();
    $('.passed_list').hide();
    $('.in_contact_list').hide();


    // let toTop = document.getElementById("to-top-btn");
    window.onscroll = function() {scrollFunction()}

    function scrollFunction() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        toTop.style.display = "block";
      } else {
        toTop.style.display = "none";
      }
    };

    $('#to-top-btn').on('click', function() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    });


});