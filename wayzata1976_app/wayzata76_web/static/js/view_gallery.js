$(document).ready(function() {

    $('a.carousel-control-prev').on('click', function() {
        $('.carousel').carousel('prev');
    });

    $('a.carousel-control-next').click(function() {
        $('.carousel').carousel('next');
    });

    $('a.gal-item-img-anchor::after')on('click', function() {
        // let imageIndex = $(this).id;
        
        $('div.carousel-item.text-center.active').removeClass('active');
        $((`div.carousel-item.text-center:nth-of-type(${$(this).attr('id')})`.addClass('active');

        $('#carousel').carousel($(this).attr('id'));
        alert('Index = ' + $(this).attr('id'));
        
      
    });


    String.prototype.format = function () {
        var a = this;
        for (var k in arguments) {
            a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
        }
        return a
    }

});