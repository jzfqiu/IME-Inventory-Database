

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
            if (this.onDp || this.onNv) {displayDropdown()}
            else {hideDropdown()}
        },
        set onNav(bool) {
            this.onNv = bool;
            if (this.onDp || this.onNv) {displayDropdown()}
            else {hideDropdown()}
        }
    };

    // if we hover class catNav__cat, get its id and toggle property in the status object
    let navArr = Array.from(document.getElementsByClassName('catNav__cat'));
    navArr.forEach(e => e.addEventListener('mouseenter', event => {
        displayedID = event.target.id + 'Dropdown';
        dropdownStatus.onNav = true;
    }));
    navArr.forEach(e => e.addEventListener('mouseleave', () => {
        dropdownStatus.onNav = false;
    }));

    // if we hover dropdown, toggle status object property to mark mouse location
    let dpArr = Array.from(document.getElementsByClassName('catDropdown'));
    dpArr.forEach(e => e.addEventListener('mouseenter', () => {
        dropdownStatus.onDropdown = true;
    }));
    dpArr.forEach(e => e.addEventListener('mouseleave', () => {
        dropdownStatus.onDropdown = false;
    }));

}

toggleDropdown();

// also set active to id
// if we exit dropdown AND catNav with active id, set active to null and