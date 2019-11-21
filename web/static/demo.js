// search page js

// dropdown DOMs
let doms = {
    navArr: Array.from(document.getElementsByClassName('catNav__cat')),
    dpArr: Array.from(document.getElementsByClassName('catDropdown'))
};


// dropdown behavior
function toggleDropdown() {
    // global variable of ID of dropdown currently on display
    let displayedID = null;

    // functions displaying/hiding dropdown given id
    function displayDropdown() {
        let dropdown = document.getElementById(displayedID);
        dropdown.style.display = 'flex';
    }

    function hideDropdown() {
        if (displayedID) {
            let dropdown = document.getElementById(displayedID);
            dropdown.style.display = 'none';
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
    doms.navArr.forEach(e => e.addEventListener('mouseenter', event => {
        displayedID = event.target.id + 'Dropdown';
        dropdownStatus.onNav = true;
    }));
    doms.navArr.forEach(e => e.addEventListener('mouseleave', () => {
        dropdownStatus.onNav = false;
    }));

    // if we hover dropdown, toggle status object property to mark mouse location
    doms.dpArr.forEach(e => e.addEventListener('mouseenter', () => {
        dropdownStatus.onDropdown = true;
    }));
    doms.dpArr.forEach(e => e.addEventListener('mouseleave', () => {
        dropdownStatus.onDropdown = false;
    }));
}

toggleDropdown();


let catSelection = {

    selected: {
      main: null,
      cat1: [],
      cat2: [],
      cat3: [],
      cat4: [],
      cat5: []
    },

    toJSON: function (){
        return JSON.stringify(this.selected)
    },

    monitor: function(){
        doms.dpArr.forEach(e => e.addEventListener('click', event => {
            console.log(event.target)
        }))
    }



};

catSelection.monitor();

