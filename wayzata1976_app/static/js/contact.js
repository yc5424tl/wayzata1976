$(document).ready(function() {

    $('#spouse-row').hide();

    $('.form-check-input').change(function() {
        if ($("input[type=checkbox]:checked").length) {
            $('#spouse-row').show();
        }
        else {
            $('#spouse-row').hide();
        }
    });
});