// base.js
// login and logout control

$(document).ready(function(){

    const overlayLoginParentDOM = $('#nav-login-overlay');

    $('#nav-login').click(function (event) {
        event.preventDefault();
        overlayLoginParentDOM.html(`   
            <div id="login-overlay">
                <p>Enter access code:</p>
                <button id="login-overlay-close">X</button>
                <form id="login-overlay-form">
                    <input type=text id="nav-login-key" name=login_key>
                    <input type="submit" id="nav-login-submit">
                </form>
            </div>
        `);
    });

    overlayLoginParentDOM.on('click', "#nav-login-submit", function (event) {
        event.preventDefault();
        // console.log($('#nav-login-key').val());
        $.post("/ajax/login", {'login_key': $('#nav-login-key').val()})
            .done(function (data) {
                console.log(data);
                const response = JSON.parse(data);
                if (response.success === true) {
                    window.location.replace('/');
                } else {
                    alert('Login key incorrect!');
                }
            })
    });

    overlayLoginParentDOM.on('click', "#login-overlay-close", function (event) {
        overlayLoginParentDOM.empty();
    })

});
