
$(document).ready(function() {

    let windowXS = window.matchMedia("(max-width:575px)");
    let windowSM = window.matchMedia("(min-width:576px) and (max-width:767px)");
    let windowMD = window.matchMedia("(min-width:768px) and (max-width:991px)");
    let windowLG = window.matchMedia("(min-width:992px) and (max-width:1199px)");
    let windowXL = window.matchMedia("(min-width:1200px)");


    // function index_thumbnails() {
    //     let thumbnails = document.getElementsByClassName('thumbnail-anchor');
    //     for (let i = 0; i <= thumbnails.length; i++) {
    //         thumbnails[i].dataset.index = i
    //     }
    // }


    function updateModal() {

        if (windowXS.matches || windowSM.matches) {
            $('.modal-dialog').removeClass().addClass('modal-dialog modal-sm modal-dialog-centered');
        };

        if (windowMD.matches) {
            $('.modal-dialog').removeClass().addClass('modal-dialog modal-dialog-centered');
        };

        if (windowLG.matches) {
            $('.modal-dialog').removeClass().addClass('modal-dialog modal-lg modal-dialog-centered');
        };

        if (windowXL.matches) {
            $('.modal-dialog').removeClass().addClass('modal-dialog modal-xl modal-dialog-centered');
        };

        return;
    }
    // index_thumbnails();

    updateModal();

    window.onresize = updateModal;


    // $('a.thumbnail-anchor').on('click', function() {
    //     let target_index = $(this).dataset.index;
    //     document.getElementsByClassName('image-thumbnail').removeClass('active');
    //     let carousel_item = document.querySelector(`carousel-item:nth-child(${target_index})`);
    //     $(carousel_item).addClass('active');
    //     $('#galleryModal').carousel(parseInt(target_index));
    // })


    $('.carousel').on('slide.bs.carousel', function() {

        $(this).carousel('cycle');

        $('#galleryModal').modal('handleUpdate');

        if (window.innerHeight > window.innerWidth) {
            $('.modal-dialog').css('width:auto;height:90%;');
        };

        if (window.innerHeight < window.innerWidth) {
            $('.modal-dialog').css('width:90%;height:auto;');
        };
    })

})