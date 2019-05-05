// edit.js

$(document).ready(function(){

    var fieldCounts = 3


    // control addField button behavior in /edit/..
    $("#addField").click(function(){
        fieldCounts++;

        var new_field = '<div id="editField' + fieldCounts +
        '"><input class="field" type="text" name="key' + fieldCounts +
        '">: <input class="field" type="text" name="value'+ fieldCounts +
        '"> <button class="delFieldButton" type="button" id="delField' + fieldCounts +
        '">x</button><br></div>'

        $("#editFields").append(new_field);
    });


    // 'on' method to make sure event handler is attached to dynamically created elements
    // method attached to '#editField' because it's the closest static parent element
    $('#editFields').on('click', '.delFieldButton', function(){
        var del_field_id = 'editField'+$(this).attr('id').charAt(8);
        $('#'+del_field_id).remove();
        fieldCounts--;
    });


    // prevent submitting empty field
    $('#submitField').click(function(e){
        $('.field').each(function(){
            if ($(this).val() === '') {
                alert('Field cannot be empty!');
                e.preventDefault();
                return false;
            };
        });
    });


});