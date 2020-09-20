// script for navbar, loaded in every page


// helper: parse a single dom node from string
function parseDOM(str) {
    var parser = new DOMParser();
    return parser.parseFromString(str, "text/html").body.firstChild;
}

// Toggle login overlay
var loginButton = document.querySelector('#login-trigger');
if (loginButton != null) {
    loginButton.addEventListener('click', ()=>{
        overlayWrapper.style.display = 'block';
    })
}

// Toggle display of overlay
var overlayWrapper = document.querySelector('.overlay');
document.querySelector('.overlay').addEventListener('click', (e)=>{
    if (e.target.id=="overlay-background")
        overlayWrapper.style.display = 'none';
})
document.getElementById('cancel-btn').addEventListener('click', (e)=>{
    overlayWrapper.style.display = 'none';
})


// global state for login/register mode
var loginMode = 'login';
// toggle register mode 
// (add access code, password check, and register mode identifier)
var registerSwitch = document.getElementById('register-switch');
registerSwitch.addEventListener('click', ()=>{
    document.getElementById('login-welcome').innerHTML = 'Register Account';
    document.getElementById('login-block').style.display = 'none';
    document.getElementById('return-btn').style.display = 'block';
    var registerBlocks = document.getElementsByClassName('register-block');
    for (var i = 0; i < registerBlocks.length; i++) 
        registerBlocks[i].style.display = 'block';
    loginMode = 'register';
})
// back to login mode
var loginSwitch = document.getElementById('return-btn');
loginSwitch.addEventListener('click', ()=>{
    document.getElementById('login-welcome').innerHTML = 'Welcome Back';
    document.getElementById('login-block').style.display = 'block';
    document.getElementById('return-btn').style.display = 'none';
    var registerBlocks = document.getElementsByClassName('register-block');
    for (var i = 0; i < registerBlocks.length; i++) 
        registerBlocks[i].style.display = 'none';
    loginMode = 'login';
    document.getElementById('confirmation-fail').style.display = 'none';
})


// login form submit
var loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', (e)=>{    
    e.preventDefault();
    var formData = new FormData(loginForm);
    // confirm-password validation
    if (formData.get('password') !== formData.get('confirm-password')){
        document.getElementById('confirmation-fail').style.display = 'block';
        return;
    } else {
        document.getElementById('confirmation-fail').style.display = 'none';
    }
    fetch('/fetch/'+loginMode, {
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