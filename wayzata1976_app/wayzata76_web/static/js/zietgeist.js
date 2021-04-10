$(document).ready(function() {
    const btns = document.querySelectorAll('.btn-neumo');
    alert(length(btns) + '!')

    for (let btn of btns) {
        btn.onclick = () => btn.classList.toggle('active');
    }
})