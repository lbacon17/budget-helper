$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('.datepicker').datepicker({
        format: "mmm-dd, yyyy",
        yearRange: 3,
        maxDate: +0,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
});

// $(window).load(function(){
//     $('.preloader-wrapper').fadeOut(3500);
// });