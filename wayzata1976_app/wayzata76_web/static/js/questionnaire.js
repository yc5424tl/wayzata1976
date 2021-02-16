$(document).ready(function() {

    $('#other-div').hide();

    $('#music-select').change(function() {
        if ($(this).val() === 'other') {
            $('#other-div').show();
        }
        else {
            $('#other-div').hide();
        }
    });
});
