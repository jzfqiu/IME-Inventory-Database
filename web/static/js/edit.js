// edit form behavior


// helper function to add event listener to each element in the class
function addEventListenerByClass(className, event, f){
    var arr = Array.from(document.getElementsByClassName(className));
    arr.forEach(element=>{
        element.addEventListener(event, e=>f(e))
    })
}


// preventDefault for existing buttons
addEventListenerByClass('edit-remove-li', 'click', e=>e.preventDefault())
addEventListenerByClass('edit-add-li', 'click', e=>e.preventDefault())

// attach handler to parent node
addEventListenerByClass('edit-dynamic-ul', 'click', e=>{
    var ul = e.currentTarget;
    var button = e.target
    if (button.className=="edit-remove-li" && button.parentNode.nodeName=="LI"){
        ul.removeChild(button.parentNode)
    } else if (button.className=="edit-add-li") {
        var newLi = document.createElement("li");
        newLi.innerHTML = '<button class="edit-remove-li">&times;</button>'+
                            '<input type="text" name="features" value=""/>'
        ul.insertBefore(newLi, button.parentNode);
    }
})
