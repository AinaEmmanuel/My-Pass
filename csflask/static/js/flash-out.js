$(function() {
$('#flash').hide().delay(0).fadeIn('normal', function() {
    $(this).delay(2500).fadeOut();
    });
});