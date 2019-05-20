// search.js
// search bar customization, ajax and stuff

$(document).ready(function(){

    $('#searchType').change(function () {
        const newFilter = $(this).val();
        $.ajax("/ajax/change_search_filter/" +  newFilter);
        console.log(`[AJAX] Search type changed to ${newFilter}`)
    });

    $('#searchBox').keyup(function () {
        const keywords = $(this).val();
        const search_type = $('#searchType').val();
        if (keywords) {
            $.ajax(`/ajax/search_bar_suggestion/${search_type}/${keywords}`)
                .done(function (data) {
                    const suggestions = JSON.parse(data);
                    const suggestionsList = document.createElement('ul');
                    for (name of suggestions){
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<a>${name}</a>`;
                        suggestionsList.appendChild(listItem)
                    }
                    console.log(suggestionsList);
                    $('#suggestions').empty().append(suggestionsList);
                })
        } else {
            $('#suggestions').empty()
        }
    });

});