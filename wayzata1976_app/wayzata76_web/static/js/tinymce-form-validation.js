window.onload = function () {
    const form = document.getElementById('form');
    const editor = document.getElementById('tinymce');
    $(editor).attr('required', 'required');

    form.addEventListener('submit', () => {
        editor.on('change', function () {
            tinymce.triggerSave();
        });
    });
}
