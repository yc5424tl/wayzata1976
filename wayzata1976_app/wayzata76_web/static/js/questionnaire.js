$(document).ready(function() {

    $('#otherDiv').hide();

    $('#musicSelect').change(function() {
        if ($(this).val() === 'other') {
            $('#otherDiv').show();
        }
        else {
            $('#otherDiv').hide();
        }
    });
});
