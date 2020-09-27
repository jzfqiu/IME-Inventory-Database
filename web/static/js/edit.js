// edit form behavior



let imageList = document.querySelector('.edit-images-list');
// delete image 
imageList.addEventListener('click', (e)=>{
    let child = e.target.parentNode;
    if (e.target.tagName=='IMG')
        child = child.parentNode;
    e.currentTarget.removeChild(child);
})

// cloudinary widget behavior
var myWidget = cloudinary.createUploadWidget({
    cloudName: 'ime-inventory-db', 
    uploadPreset: 'unsigned_preset'}, (error, result) => { 
        if (!error && result && result.event === "success") { 
            let newItem = document.createElement('div');
            newItem.innerHTML = `
                <div><img src="/static/assets/trash.webp"></div>
                <img src="${result.info.url}">
                <input type="hidden" name="images" value="${result.info.url}">`;
            newItem.className = "edit-images-item";
            console.log(newItem);
            imageList.appendChild(newItem);
        }
    }
);
document.getElementById("upload_widget").addEventListener("click", function(){
    myWidget.open();
}, false);





// helper function to add event listener to each element in the class
function addEventListenerBySelector(selector, event, f){
    var arr = Array.from(document.querySelectorAll(selector));
    arr.forEach(element=>{
        element.addEventListener(event, e=>f(e))
    })
}


function makeJsonHeader(fetchUrl, jsonData){
    let hdr = new Headers();
    hdr.append('Content-Type', 'application/json');
    let req = new Request(fetchUrl, {
        method: 'POST',
        body: JSON.stringify(jsonData),
        headers: hdr
    });
    return req;
}




// preventDefault for existing buttons
addEventListenerBySelector('.edit-remove-li', 'click', e=>e.preventDefault());
addEventListenerBySelector('.edit-add-li', 'click', e=>e.preventDefault());

// attach handler to parent node
addEventListenerBySelector('.edit-dynamic-ul', 'click', e=>{
    var ul = e.currentTarget;
    var button = e.target
    if (button.className=="edit-remove-li" && button.parentNode.nodeName=="LI"){
        ul.removeChild(button.parentNode)
    } else if (button.className=="edit-add-li") {
        var newLi = document.createElement("li");
        newLi.innerHTML = '<button class="edit-remove-li" type="button">&times;</button>'+
                            '<input type="text" name="features" value=""/>'
        ul.insertBefore(newLi, button.parentNode);
    }
});


// get options from dictionary and insert them as children of <select>
// ulDom: the ul DOM container
// prevSelections: list of selections in previous level of inputs
// selectedOption: if editing existing entries, checkmark currently selected option
function getInsertOptions(ulDom, prevSelections, selectedOption=null) {
    let listOfOptions, cat, bucket;
    ulDom.innerHTML = "";
    // get category dictionary
    fetch("/fetch/edit/categories")
    .then(response => response.json())
    .then(cats_dict => {
        if (prevSelections.length == 1){ 
            // if only cat has been selected
            cat = cats_dict[prevSelections[0]]
            if (cat != null)
                listOfOptions = Object.keys(cat['children']);
        } else { 
            // if both cat and bucket are selected
            cat = cats_dict[prevSelections[0]]
            if (cat != null)
                bucket = cat["children"][prevSelections[1]]
            if (cat!=null && bucket!=null)
                listOfOptions = bucket["children"];
        };
        if (listOfOptions == null) return;
        listOfOptions.map(option => {
            var optionDom = document.createElement('li');
            optionDom.setAttribute('value', option);
            optionDom.innerHTML = option;
            if (option==selectedOption) optionDom.selected = true;
            optionDom.addEventListener( 'click', e=>fillInput(e.target))
            ulDom.appendChild(optionDom);
        });
    });
}

// initialize options, run once each refresh
var editCat = document.getElementById('edit-cat');
var editBucket = document.getElementById('edit-bucket');
var editItem = document.getElementById('edit-item');
var editCampus = document.getElementById('edit-camp');
var editSubCampus = document.getElementById('edit-subCamp');



// fill input when dropdown item is clicked
// navigates to target's (li) parent's (ul) sibling (input)
function fillInput(target) {
    var choice = target.innerHTML;
    var inputDom = target.parentNode.nextElementSibling;
    inputDom.value = choice;
}
addEventListenerBySelector('#edit-category li', 'click', e=>fillInput(e.target))


// show dropdown when mouse focus on input
addEventListenerBySelector('.edit-cat-input', 'focusin', e=>{
    var curCat = editCat.value;
    if (e.target.id == "edit-cat") {
        document.getElementById('edit-cat-options').style.display = 'inline-block'
    } else if (e.target.id == "edit-bucket") {
        document.getElementById('edit-bucket-options').style.display = 'inline-block'
    } else if (e.target.id == "edit-item") {
        document.getElementById('edit-item-options').style.display = 'inline-block'
    } else if (e.target.id == "edit-camp") {
        document.getElementById('edit-camp-options').style.display = 'inline-block'
    }
})


// detect change in selections
function getNextOptions(e) {
    var bucketOptions = document.getElementById("edit-bucket-options")
    var itemOptions = document.getElementById("edit-item-options")
    if (e.target.id == "edit-cat") {
        // empty children categories inputs
        editBucket.value = ""
        editItem.value = ""
        // empty children categories option list
        bucketOptions.innerHTML = ""
        itemOptions.innerHTML = ""
        // insert new options
        getInsertOptions(editBucket.previousElementSibling, [editCat.value]);
        document.getElementById('edit-cat-options').style.display = 'none'
    } else if (e.target.id == "edit-bucket") {
        editItem.value = ""
        itemOptions.innerHTML = ""
        getInsertOptions(editItem.previousElementSibling, [editCat.value, editBucket.value]);
        document.getElementById('edit-bucket-options').style.display = 'none'
    } else if (e.target.id == "edit-item") {
        document.getElementById('edit-item-options').style.display = 'none'
    } else if (e.target.id == "edit-camp") {
        var curCamp = editCampus.value;
        // getInsertOptions(editSubCampus, ["Campus", curCamp]);
        // TODO: fix campus
        document.getElementById('edit-camp-options').style.display = 'none'
    }
}
/* use setTimeout to queue the focusout event after 100 ms because focusout event seems  
   to take precedence before click event which causes dom to un-display and click event
   never captured. This order seems to be enforced by browsers and may not be the same 
   everywhere. */
addEventListenerBySelector('.edit-cat-input', 'focusout', e=>{setTimeout(()=>getNextOptions(e), 200)})




// auto update google map
let timeout = null;
let editLocation = document.getElementById('edit-location');
let mapApi = document.getElementById('edit-location-api');
let editLocationInput = document.getElementById("edit-location-input");
editLocation.addEventListener('keyup', e => {
    clearTimeout(timeout);
    timeout = setTimeout(function () {
        // replace one or more characters that is not letter/number to '+'
        const regex = /[^A-Za-z0-9]+/g 
        let cleaned_input = editLocationInput.value.replace(regex, '+')
        let prevSrc = mapApi.src;
        if (cleaned_input)
            mapApi.src = prevSrc.substring(0, prevSrc.indexOf("&q=")+3)+cleaned_input;
    }, 1000);
});



// cleanup data from form using FormData class
function getFormData(form){
    var formData = new FormData(form);
    var dynamicUl = document.getElementsByClassName('edit-dynamic-ul');
    var formObj = {}
    for (var key of formData.keys()) {
        if (key=='features' || key=='images' || key=='applications') { 
            // if key has not been visited
            formObj[key] = formData.getAll(key);
        } else { // else the key points to a list
            formObj[key] = formData.get(key);
        }
    }
    return JSON.stringify(formObj);
}

// submit form
var editForm = document.getElementById('edit-form');
editForm.addEventListener('submit', e=>{
    e.preventDefault();
    var currentUrl = window.location.href;
    var formJSON = getFormData(editForm);
    console.log(formJSON)
    var req = makeJsonHeader(currentUrl, formJSON, 'POST');
    fetch(req)
    .then(response=>response.json())
    .then(data => {
        if (data['success'])
            window.location.href = data['return_url'];
    })
})

	