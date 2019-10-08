

$(document).ready(function(){

    $('.catNav__cat, .catDropdown').hover(
        function () {
            $('.catDropdown').css('display', 'flex');
        },
        function () {
            $('.catDropdown').css('display', 'none');
        }
    )

});