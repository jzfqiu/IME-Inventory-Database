

$(document).ready(function(){


    // $('.catNav__cat')
    //     .mouseover( function () {
    //         let hover_nav = $(this).attr('id').charAt(3);
    //         $('#catDropdown'+hover_nav).css('display', 'flex');
    //     });
    //
    // $('.catDropdown')
    //     .mouseout(function () {
    //         let hover_nav = $(this).attr('id').charAt(11);
    //         $('#catDropdown'+hover_nav).css('display', 'none');
    //     });
    let hover_nav = -1;

    $('.catNav__cat, .catDropdown').hover(
        function () {
            hover_nav = $(this).attr('id').charAt(3);
            $('#cat'+hover_nav).addClass('catNav__cat--hover');
            $('#cat'+hover_nav+'Dropdown').css('display', 'flex');
        },
        function () {
            $('#cat'+hover_nav).removeClass('catNav__cat--hover');
            $('#cat'+hover_nav+'Dropdown').css('display', 'none');
        });




});