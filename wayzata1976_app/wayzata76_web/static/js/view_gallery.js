// sm-576+  md 768+   lg 992+  xl 1200+

$(document).ready(function() {

    let windowXS = window.matchMedia("(max-width:575px)");
    let windowSM = window.matchMedia("(min-width:576px) and (max-width:767px)");
    let windowMD = window.matchMedia("(min-width:768px) and (max-width:991px)");
    let windowLG = window.matchMedia("(min-width:992px) and (max-width:1199px)");
    let windowXL = window.matchMedia("(min-width:1200px)");

    $('.modal-content').resizable();
    $('.model-dialog').draggable();

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

    updateModal();

    window.onresize = updateModal;

    $('.carousel').on('slide.bs.carousel', function() {
        // $('#galleryModal').data('bs.modal').handleUpdate()
       
        $(this).carousel('cycle');
        $(this).carousel({
            interval: 3000
        })
  
        $('#galleryModal').modal('handleUpdate');
        

        if (window.innerHeight > window.innerWidth) {
            $('.modal-dialog').css('width:auto;height:90%;');
        };
    
        if (window.innerHeight < window.innerWidth) {
            $('.modal-dialog').css('width:90%;height:auto;');
        };
    })

   

})