$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
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
    $('.preloader-wrapper').fadeOut('slow');
    $('.modal').modal()
});

function confirmDeletion() {
    // var popup = document.getElementById("popup");
    // popup.classList.toggle("show");
    confirm("Are you sure you want to delete your account?");
}