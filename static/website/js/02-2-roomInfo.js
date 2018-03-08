$(document).ready(function() {

    $('#select_date').datepicker({
        dateFormat: 'yy-mm-dd',
        monthNames: ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'],
    });

    var swiper = new Swiper('.swiper-container', {
        pagination: '.swiper-pagination',
        paginationType: 'fraction',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        paginationClickable: true,
//        spaceBetween: 500,
        centeredSlides: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        effect: 'fade',
        loop: true
    });

    $(".backToTop").click(function () {
        console.log(11);
        scrollTo(0,0);
    });
});