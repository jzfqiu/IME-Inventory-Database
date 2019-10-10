

$(document).ready(function(){

    let hover_nav = -1;

    $('.catNav__cat, .catDropdown').hover(
        function () {
            hover_nav = $(this).attr('id').charAt(3);
            $('#cat'+hover_nav).addClass('catNav__cat--hover');
            $('#cat'+hover_nav+'Dropdown').css('display', 'flex');
            $('#test-block').text('Select category choices in dropdown menu. ' +
                'There can be at most 3 layers of choices (e.g. Material-Ceramics-Glasses) ' +
                'and at least 2 layers (e.g. Campus-Chicago). ' +
                'Users will be able to select an entire bucket as well.')
        },
        function () {
            $('#cat'+hover_nav).removeClass('catNav__cat--hover');
            $('#cat'+hover_nav+'Dropdown').css('display', 'none');
            $('#test-block').text('')
        });

    let selected_division = 'all';
    $('.sidebar-divisions__division').click(function () {
        let div_id = $(this).attr('id');
        if (div_id !== selected_division) {
            $('#'+selected_division).removeClass('sidebar-divisions__division--selected');
            $('#'+div_id).addClass('sidebar-divisions__division--selected');
            selected_division = div_id;
        }
    });

    $('.sidebar-refine__wrapper').hover(
        function () {
            $('#test-block').text('This section will dynamically display selected choices in categories above.' +
                'Individual choices can also be deselected here.')
        },
        function () {
            $('#test-block').text('')
        }
    );

    $('.sidebar-divisions__wrapper').hover(
        function () {
            $('#test-block').text('Select a division to search in.')
        },
        function () {
            $('#test-block').text('')
        }
    );

    $('.result-block').hover(
        function () {
            $('#test-block').text('Results will be listed here. ' +
                'When no category is selected, display the most viewed equipments.')
        },
        function () {
            $('#test-block').text('')
        }
    )

});