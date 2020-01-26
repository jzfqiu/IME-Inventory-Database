// search page js

// dropdown DOMs
let DOMs = {
    navArr: Array.from(document.getElementsByClassName('sidebar-catNav__cat')),
    dpArr: Array.from(document.getElementsByClassName('catDropdown')),
    choiceArr: Array.from(document.getElementsByClassName('catDropdown__item')),
    catRefineWrapper: document.getElementsByClassName('sidebar-refine__wrapper').item(0),
    linkArr: Array.from(document.getElementsByClassName('result-block-name__link')),
    overlayWrapper: document.getElementsByClassName('overlay').item(0),
};

let helpers = {

    makeUL: function(array, className) {

        // return list;
    },

    buildDOM: function (tag, className=null, text=null) {
        let resDOM = document.createElement(tag);
        if (className) resDOM.classList.add(className);
        if (text) resDOM.appendChild(document.createTextNode(text));
        return resDOM;
    }
};


// dropdown behavior
function toggleDropdown() {
    // global variable of ID of dropdown currently on display
    let displayedID = null;

    // functions displaying/hiding dropdown given id
    function displayDropdown() {
        let dropdown = document.getElementById(displayedID + 'Dropdown');
        let nav = document.getElementById(displayedID);
        dropdown.style.display = 'flex';
        nav.classList.add('sidebar-catNav__cat--hover')
    }

    function hideDropdown() {
        if (displayedID) {
            let dropdown = document.getElementById(displayedID+ 'Dropdown');
            let nav = document.getElementById(displayedID);
            dropdown.style.display = 'none';
            nav.classList.remove('sidebar-catNav__cat--hover')
        }
    }

    // object with setters to respond to status change
    let dropdownStatus = {
        onDp : false,
        onNv : false,
        set onDropdown(bool) {
            this.onDp = bool;
            if (this.onDp || this.onNv) {displayDropdown();}
            else {hideDropdown();}
        },
        set onNav(bool) {
            this.onNv = bool;
            if (this.onDp || this.onNv) {displayDropdown();}
            else {hideDropdown();}
        }
    };

    // if we hover class catNav__cat, get its id and toggle property in the status object
    DOMs.navArr.forEach(e => e.addEventListener('mouseenter', event => {
        displayedID = event.target.id;
        dropdownStatus.onNav = true;
    }));
    DOMs.navArr.forEach(e => e.addEventListener('mouseleave', () => {
        dropdownStatus.onNav = false;
    }));

    // if we hover dropdown, toggle status object property to mark mouse location
    DOMs.dpArr.forEach(e => e.addEventListener('mouseenter', () => {
        dropdownStatus.onDropdown = true;
    }));
    DOMs.dpArr.forEach(e => e.addEventListener('mouseleave', () => {
        dropdownStatus.onDropdown = false;
    }));
}

toggleDropdown();


// class controlling dropdown selection and async requests
let catSelection = {

    selected: {},

    toJSON: function (obj){
        return JSON.stringify(obj)
    },

    monitor: function(){
        DOMs.choiceArr.forEach(e => e.addEventListener('click', event => {
            let choiceStr = event.target.id.split(":");
            let choiceCat = choiceStr[0];

            let choiceItemStr = choiceStr[1];
            let choiceBucket = choiceItemStr.split("-")[0];
            let choiceItem = choiceItemStr.split("-")[1];

            // push change to class variable and DOM
            this.pushChange(choiceCat, choiceBucket, choiceItem);
        }))
    },

    objToDOM: function(obj) {
        let refCat__wrapper = document.createElement("ul");
        for (let cat in obj) {
            let refCat = helpers.buildDOM("li", "sidebar-refine-cat", "");

            refCat.appendChild(helpers.buildDOM("div", "sidebar-refine-cat__text", cat));

            let refBucket__wrapper = document.createElement("ul");
            for (let bucket in obj[cat]) {
                let refBucket = helpers.buildDOM("li", "sidebar-refine-bucket", bucket);

                let refItem__wrapper = document.createElement('ul');
                for (let i = 0; i < obj[cat][bucket].length; i++) {
                    let item = helpers.buildDOM('li', "sidebar-refine-item");
                    item.appendChild(helpers.buildDOM('div', "sidebar-refine-item__text", obj[cat][bucket][i]));
                    item.appendChild(helpers.buildDOM('div', "sidebar-refine-item__x", "x"));
                    item.addEventListener('click', () => {this.pushChange(cat, bucket, obj[cat][bucket][i])});
                    refItem__wrapper.appendChild(item);
                }
                refBucket.appendChild(refItem__wrapper);
                refBucket__wrapper.appendChild(refBucket);
            }
            refCat.appendChild(refBucket__wrapper);
            refCat__wrapper.appendChild(refCat)
        }

        return refCat__wrapper;
    },

    pushChange: function (cat, Bucket, item) {
        if (cat in this.selected) {
            let curCat = this.selected[cat];
            if (Bucket in curCat) {
                let curBucket = curCat[Bucket];
                let idx = curBucket.indexOf(item);
                if (idx !== -1) {
                    // deselect radio button on dropdown
                    document.getElementById(cat+':'+Bucket+'-'+item).checked = false;
                    // delete item from selected
                    curBucket.splice(idx, 1);
                    // check if Bucket and cat is empty, if so execute nested delete
                    if (curBucket.length === 0) {
                        delete curCat[Bucket];
                        if (Object.entries(curCat).length === 0) {
                            delete this.selected[cat];
                        }
                    }
                } else {
                    // add item to selected
                    curBucket.push(item)
                }
            } else {
                // add Bucket and item to selected
                curCat[Bucket] = [item];
            }
        } else {
            this.selected[cat] = {[Bucket]: [item]};
        }
        // console.log(this.toJSON(this.selected));
        let node = this.objToDOM(this.selected);
        DOMs.catRefineWrapper.innerHTML = '';
        DOMs.catRefineWrapper.appendChild(node);
    },
};


// TODO: color code blocks by campus, user defined sorting


catSelection.monitor();

let toggleOverlay = {

    attachListener: function(){
        DOMs.linkArr.forEach(e => e.addEventListener('click', e => {
            DOMs.overlayWrapper.style.display = 'block';
        }));
        DOMs.overlayWrapper.addEventListener('click', e => {
            DOMs.overlayWrapper.style.display = 'none';
        })
    }

};

toggleOverlay.attachListener();



