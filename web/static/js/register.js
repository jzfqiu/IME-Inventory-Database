// register form submit
var registerForm = document.querySelector('.register-form');
registerForm.addEventListener('submit', (e)=>{    
    e.preventDefault();
    var formData = new FormData(registerForm);

    // make sure passwords match
    if (formData.get('password') != formData.get("confirm-password")){
        document.getElementById('fail-message').innerHTML = "Passwords do not match. Please try again.";
        return;
    }

    console.log(formData.get('password'))
    console.log(formData.get('confirm-password'))
    fetch('/register', {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then(result => {
        console.log(result)
        if (result['success']) {
            window.history.back();
        } else {
            console.log(result['message']);
            document.getElementById('fail-message').innerHTML = result['message'];
        }
    })
})