// search page js

// dropdown DOMs
let DOMs = {
    navArr: Array.from(document.getElementsByClassName('sidebar-catNav__cat')),
    dpArr: Array.from(document.getElementsByClassName('catDropdown')),
    choiceArr: Array.from(document.getElementsByClassName('catDropdown__item')),
    catRefineWrapper: document.getElementsByClassName('sidebar-refine__wrapper').item(0),
    linkArr: Array.from(document.getElementsByClassName('result-block-name__link')),
    resultWrapper: document.querySelector('.result'),
};

let helpers = {
    buildDOM: function (tag, className = null, text = null) {
        let resDOM = document.createElement(tag);
        if (className) resDOM.classList.add(className);
        if (text) resDOM.appendChild(document.createTextNode(text));
        return resDOM;
    }
};

var input = document.getElementById("top-searchBox");
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("top-searchButton").click();
    }
});


// dropdown behavior
// TODO: refractor to object
class ToggleDropdown {
    constructor() {
        // global variable of ID of dropdown currently on display
        this.displayedID = null;
        this.onDp = false;
        this.onNv = false;
    }

    // functions displaying/hiding dropdown given id
    displayDropdown() {
        let dropdown = document.getElementById(this.displayedID + 'Dropdown');
        let nav = document.getElementById(this.displayedID);
        dropdown.style.display = 'flex';
        nav.classList.add('sidebar-catNav__cat--hover')
    }

    hideDropdown() {
        if (this.displayedID) {
            let dropdown = document.getElementById(this.displayedID + 'Dropdown');
            let nav = document.getElementById(this.displayedID);
            dropdown.style.display = 'none';
            nav.classList.remove('sidebar-catNav__cat--hover')
        }
    }

    // setters to respond to status change
    set onDropdown(bool) {
        this.onDp = bool;
        if (this.onDp || this.onNv) { this.displayDropdown(); }
        else { this.hideDropdown(); }
    }

    set onNav(bool) {
        this.onNv = bool;
        if (this.onDp || this.onNv) { this.displayDropdown(); }
        else { this.hideDropdown(); }
    }

    attachListener() {
        // if we hover class catNav__cat, get its id and toggle property in the status object
        DOMs.navArr.forEach(e => e.addEventListener('mouseenter', event => {
            this.displayedID = event.target.id;
            this.onNav = true
        }));
        DOMs.navArr.forEach(e => e.addEventListener('mouseleave', () => {
            this.onNav = false
        }));

        // if we hover dropdown, toggle status object property to mark mouse location
        DOMs.dpArr.forEach(e => e.addEventListener('mouseenter', () => {
            this.onDropdown = true
        }));
        DOMs.dpArr.forEach(e => e.addEventListener('mouseleave', () => {
            this.onDropdown = false
        }));
    }
}

let td = new ToggleDropdown();
td.attachListener();


// controlling dropdown selection and async requests
// TODO: refractor to object 
class CatSelection {
    constructor() {
        let previouslySelected = JSON.parse(sessionStorage.getItem('selectedCats'));
        this.selected = previouslySelected == null ? {} : previouslySelected;
        this.clearButton = helpers.buildDOM('button', "sidebar-refine-clearButton", "Clear");
        this.submitButton = helpers.buildDOM('button', "sidebar-refine-submitButton", "Submit");
        this.clearButton.addEventListener('click', () => { this.clearSelection() });
        this.submitButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.submitSelection('1');
        });
        let keywords = sessionStorage.getItem('keywords');
        document.getElementById('top-searchBox').value = keywords;
    }


    monitor() {
        DOMs.choiceArr.forEach(e => e.addEventListener('click', event => {
            let choiceStr = event.target.id.split(":");
            let choiceCat = choiceStr[0];

            let choiceItemStr = choiceStr[1];
            let choiceBucket = choiceItemStr.split("-")[0];
            let choiceItem = choiceItemStr.split("-")[1];

            // push change to class variable and DOM
            this.pushChange(choiceCat, choiceBucket, choiceItem);
        }));
        document.getElementById("top-searchButton").addEventListener('click', ()=>{
            this.submitSelection(1);
        })
    }

    objToDOM(obj) {
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
                    item.addEventListener('click', () => { this.pushChange(cat, bucket, obj[cat][bucket][i]) });
                    refItem__wrapper.appendChild(item);
                }
                refBucket.appendChild(refItem__wrapper);
                refBucket__wrapper.appendChild(refBucket);
            }
            refCat.appendChild(refBucket__wrapper);
            refCat__wrapper.appendChild(refCat)
        }
        refCat__wrapper.appendChild(this.clearButton);
        refCat__wrapper.appendChild(this.submitButton);
        return refCat__wrapper;
    }

    refreshSelectionDOM() {
        DOMs.catRefineWrapper.innerHTML = '';
        // check if object is empty, and if not, dont append the buttons
        if (Object.entries(this.selected).length !== 0) {
            let node = this.objToDOM(this.selected);
            DOMs.catRefineWrapper.appendChild(node);
        }
    }

    pushChange(cat, Bucket, item) {
        if (cat in this.selected) {
            let curCat = this.selected[cat];
            if (Bucket in curCat) {
                let curBucket = curCat[Bucket];
                let idx = curBucket.indexOf(item);
                if (idx !== -1) {
                    // deselect radio button on dropdown
                    document.getElementById(cat + ':' + Bucket + '-' + item).checked = false;
                    // delete item from selected
                    curBucket.splice(idx, 1);
                    // check if Bucket and cat is empty, if so execute nested delete
                    if (curBucket.length === 0) {
                        delete curCat[Bucket];
                        if (Object.entries(curCat).length === 0) delete this.selected[cat];
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
            this.selected[cat] = { [Bucket]: [item] };
        }
        sessionStorage.setItem('selectedCats', JSON.stringify(this.selected));
        this.refreshSelectionDOM();
    }

    clearSelection() {
        this.selected = {};
        sessionStorage.setItem('selectedCats', JSON.stringify(this.selected));
        this.refreshSelectionDOM();
        this.submitSelection('1');
    }

    submitSelection(page = '1') {
        let keywords = document.getElementById('top-searchBox').value;
        sessionStorage.setItem('keywords', keywords);
        let reqBody = { ...this.selected, ...{ 'keywords':  keywords} }
        let hdr = new Headers();
        hdr.append('Content-Type', 'application/json');
        let req = new Request('/fetch/page/' + page, {
            method: 'POST',
            body: JSON.stringify(reqBody),
            headers: hdr
        });
        fetch(req).then((response) => {
            if (response.ok) {
                response.text().then((dom) => {
                    DOMs.resultWrapper.innerHTML = dom;
                    Array.from(document.getElementsByClassName("result-pages__link")).forEach(
                        (e) => e.addEventListener('click', (e) => {
                            this.submitSelection(e.target.id)
                        }))
                    this.refreshSelectionDOM();
                })
            }
        })
    }

}
let cat = new CatSelection();
cat.monitor();
cat.submitSelection();

