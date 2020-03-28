// script for navbar, loaded in every page


var overlayWrapper = document.querySelector('.overlay');

// Toggle login overlay
document.querySelector('#login-trigger').addEventListener('click', ()=>{
    console.log('login');
    overlayWrapper.style.display = 'block';
})
document.querySelector('.overlay').addEventListener('click', (e)=>{
    if (e.target.id=="overlay-background")
        overlayWrapper.style.display = 'none';
})
document.getElementById('cancel-btn').addEventListener('click', (e)=>{
    overlayWrapper.style.display = 'none';
})


// login form submit
var loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', (e)=>{    
    e.preventDefault();
    var formData = new FormData(loginForm);
    fetch('/fetch/login', {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then(result => {
        if (result['success']) {
            location.reload()
        } else {
            document.getElementById('login-fail').style.display = 'block';
        }
    })
})
