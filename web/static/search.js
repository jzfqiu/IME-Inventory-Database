// search.js
// search bar customization, ajax and stuff

$(document).ready(function(){

    $('#search-type').change(function () {
        const newFilter = $(this).val();
        $.ajax("/ajax/change_search_filter/" +  newFilter);
        console.log(`[AJAX] Search type changed to ${newFilter}`)
    });

    $('#search-box').keyup(function () {
        const keywords = $(this).val();
        const search_type = $('#search-type').val();
        if (keywords) {
            $.ajax(`/ajax/search_bar_suggestion/${search_type}/${keywords}`)
                .done(function (data) {
                    const suggestions = JSON.parse(data);
                    const suggestionsList = document.createElement('ul');
                    for (item of suggestions){
                        const listItem = document.createElement('li');
                        listItem.innerHTML = `<a href="${item.link}">${item.name}</a>`;
                        suggestionsList.appendChild(listItem)
                    }
                    // console.log(suggestionsList);
                    $('#suggestions').empty().append(suggestionsList);
                })
        } else {
            $('#suggestions').empty()
        }
    });

});