// edit form behavior


// helper function to add event listener to each element in the class
function addEventListenerByClass(className, event, f){
    var arr = Array.from(document.getElementsByClassName(className));
    arr.forEach(element=>{
        element.addEventListener(event, e=>f(e))
    })
}


function makeJsonHeader(fetchUrl, jsonData=null, method='GET'){
    let hdr = new Headers();
    hdr.append('Content-Type', 'application/json');
    let req = new Request(fetchUrl, {
        method: method,
        headers: hdr
    });
    if (jsonData)
        req['body'] = JSON.stringify(jsonData)
    return req;
}


// preventDefault for existing buttons
addEventListenerByClass('edit-remove-li', 'click', e=>e.preventDefault());
addEventListenerByClass('edit-add-li', 'click', e=>e.preventDefault());

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
});


// get options from dictionary and insert them as children of <select>
function getInsertOptions(selectDom, prevSelections, selectedOption=null) {
    let listOfOptions;
    // get category dictionary
    fetch(makeJsonHeader("/fetch/edit/cat"))
    .then(response => response.json())
    .then(cats_dict => {
        if (prevSelections.length == 1){ // if only cat has been selected
            listOfOptions = Object.keys(cats_dict[prevSelections[0]]);
        } else { // if both cat and bucket are selected
            listOfOptions = cats_dict[prevSelections[0]][prevSelections[1]];
        };
        selectDom.innerHTML = "";
        listOfOptions.map(option => {
            var optionDom = document.createElement('option');
            optionDom.setAttribute('value', option);
            optionDom.innerHTML = option;
            if (option==selectedOption) optionDom.selected = true;
            selectDom.appendChild(optionDom);
        });
    });
}

// initialize options, run once each refresh
var editCat = document.getElementById('edit-cat');
var editBucket = document.getElementById('edit-bucket');
var editItem = document.getElementById('edit-item');
var editCampus = document.getElementById('edit-camp');
var editSubCampus = document.getElementById('edit-subCamp');
(function (){
    var selectedCat = editCat.getAttribute('data-selected');
    var selectedBucket = editBucket.getAttribute('data-selected');
    var selectedItem = editItem.getAttribute('data-selected');
    var selectedCampus = editCampus.getAttribute('data-selected');
    var selectedSubCampus = editSubCampus.getAttribute('data-selected');
    
    for (child of editCat.children) 
        if (child.value == selectedCat) child.selected=true;

    for (child of editCampus.children) 
        if (child.value == selectedCampus) child.selected=true;
 
    getInsertOptions(editBucket, [selectedCat], selectedBucket);
    getInsertOptions(editItem, [selectedCat, selectedBucket], selectedItem);
    getInsertOptions(editSubCampus, ["Campus", selectedCampus], selectedSubCampus);
})();


// detect change in selections
addEventListenerByClass('edit-cat-select', 'change', e=>{
    var curCat = editCat.options[editCat.selectedIndex].value;
    if (e.target.id == "edit-cat") {
        getInsertOptions(editBucket, [curCat]);
        editItem.innerHTML = "";
    } else if (e.target.id == "edit-bucket") {
        var curBucket = editBucket.options[editBucket.selectedIndex].value;
        getInsertOptions(editItem, [curCat, curBucket]);
    } else if (e.target.id == "edit-camp") {
        var curCamp = editCampus.options[editCampus.selectedIndex].value;
        getInsertOptions(editSubCampus, ["Campus", curCamp]);
    }
})


// auto update google map
// var timeout = null;
// var editLocation = document.getElementById('edit-location');
// var mapApi = document.getElementById('edit-location-api');
// editLocation.addEventListener('keyup', e => {
//     clearTimeout(timeout);
//     timeout = setTimeout(function () {
//         mapApi.src;
//     }, 1000);
// });


function formToJson( form ) {
    var obj = {};
    var elements = form.querySelectorAll( "input, select, textarea" );
    for( var i = 0; i < elements.length; ++i ) {
        var element = elements[i];
        var name = element.name;
        var value = element.value;
        if( name ) {
            if (name in obj) {
                obj[name] = obj[name] instanceof Array ? [...obj[name], value] : [obj[name], value]
            }
            else obj[name] = value;
        } 
    }
    return JSON.stringify( obj );
}


// submit form
var editForm = document.getElementById('edit-form');
editForm.addEventListener('submit', e=>{
    e.preventDefault();
    var currentUrl = window.location.href;
    var formData = formToJson(editForm);
    var req = makeJsonHeader(currentUrl, formData, 'POST');
    fetch(req)
    .then(response=>response.json())
    .then(data => {
        if (data['success'])
            window.location.href = data['return_url'];
    })
})

	