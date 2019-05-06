// edit.js

$(document).ready(function(){

    var fieldCounts = {
        "featureCounts" : 1,
        "applicationCounts" : 1,
        "tagCounts" : 1
    };


    // control addField button behavior in /edit/..
    $(".addField").click(function(){

        const targetId = $(this).attr('id'); // e.g. "addApplication"
        const targetType = targetId.substring(3); // e.g. "Application"

        const newCount = ++fieldCounts[targetType.toLocaleLowerCase()+'Counts'];

        const newDivID = targetType.toLocaleLowerCase() + newCount;
        const newDelID = 'del' + targetType + newCount;

        // id="application2" name="application2"
        const new_field = (`
            <div id="${newDivID}">
                <input class="field" type="text" name="${newDivID}">
                <button class="delFieldButton" type="button" id="${newDelID}">x</button>
            </div>
        `);

        $("#"+targetType.toLocaleLowerCase()+'s').append(new_field);
    });


    // 'on' method to make sure event handler is attached to dynamically created elements
    // method attached to '#editFields' because it's the closest static parent element
    $('#editFields').on('click', '.delFieldButton', function(){
        const targetId = $(this).attr('id'); // e.g. "delApplication"
        const targetDivID = targetId.substring(3); // e.g. "Application"
        $("#"+targetDivID.toLocaleLowerCase()).remove();
        console.log("#"+targetDivID.toLocaleLowerCase())
    });


    // prevent submitting empty field
    $('#submitField').click(function(e){
        $('.field').each(function(){
            if ($(this).val() === '') {
                alert('Field cannot be empty!');
                e.preventDefault();
                return false;
            }
        });
    });


});