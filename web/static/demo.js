// search page js

// dropdown DOMs
let DOMs = {
    navArr: Array.from(document.getElementsByClassName('sidebar-catNav__cat')),
    dpArr: Array.from(document.getElementsByClassName('catDropdown')),
    choiceArr: Array.from(document.getElementsByClassName('catDropdown__item')),
    catRefineWrapper: document.getElementsByClassName('sidebar-refine__wrapper')
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
            let choiceSubCat = choiceItemStr.split("-")[0];
            let choiceItem = choiceItemStr.split("-")[1];

            // push change to class variable and DOM
            this.pushChange(choiceCat, choiceSubCat, choiceItem);
        }))
    },

    // objToDOM: function() {
    //     let cat, subCat, item;
    //     let res = [];
    //     for (cat in this.selected) {
    //         let refineCat = document.createElement("p");
    //         let refineCatText = document.createTextNode(this.selected[cat]);
    //         res.push(refineCat.appendChild(refineCatText))
    //         for (subCat in cat) {
    //
    //         }
    //     }
    // },

    pushChange: function (cat, subCat, item) {
        if (cat in this.selected) {
            let curCat = this.selected[cat];
            if (subCat in curCat) {
                let curSubCat = curCat[subCat];
                let idx = curSubCat.indexOf(item);
                if (idx !== -1) {
                    // deselect radio button on dropdown
                    document.getElementById(cat+':'+subCat+'-'+item).checked = false;
                    // delete item from selected
                    curSubCat.splice(idx, 1);
                    // check if subCat and cat is empty, if so execute nested delete
                    if (curSubCat.length === 0) {
                        delete curCat[subCat];
                        if (Object.entries(curCat).length === 0) {
                            delete this.selected[cat];
                        }
                    }
                } else {
                    // add item to selected
                    curSubCat.push(item)
                }
            } else {
                // add subCat and item to selected
                curCat[subCat] = [item];
            }
        } else {
            this.selected[cat] = {[subCat]: [item]};
        }
        console.log(this.toJSON(this.selected))
        // node = this
        // DOMs.catRefineWrapper.replaceChild()
    },


};

catSelection.monitor();

