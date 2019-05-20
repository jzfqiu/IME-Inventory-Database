// search.js
// search bar customization, ajax and stuff

$(document).ready(function(){

    $('#searchType').change(function () {
        const newFilter = $(this).val();
        $.ajax("/ajax/change_search_filter/" +  newFilter,{
            statusCode: {
                200: function() {
                    console.log( "[AJAX] Search filter changed to " +  newFilter);
                }
            }
        });
    });



});