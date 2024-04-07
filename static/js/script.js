document.addEventListener("DOMContentLoaded", function () {
    const signInForm = document.getElementById('signInForm');
    const registrationForm = document.getElementById('registrationForm');

    if (signInForm) {
        signInForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const uid = document.getElementById('uid').value;
            const password = document.getElementById('password').value;

            const signInData = {
                uid: uid,
                password: password
            };

            sendData('/SignUsr', signInData, handleSignInResponse);
        });
    }

    if (registrationForm) {
        registrationForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const name = document.getElementById('name').value;
            const uid = document.getElementById('uid').value;
            const phone = document.getElementById('phone').value;
            const age = document.getElementById('age').value;
            const password = document.getElementById('password').value;

            const registrationData = {
                name: name,
                uid: uid,
                phone: phone,
                age: age,
                password: password
            };

            sendData('/regUsr', registrationData, handleRegistrationResponse);
        });
    }

    function sendData(url, data, callback) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
        });
    }
    
    function handleSignInResponse(responseData) {
        if (responseData.success) {
            alert('Sign In successful');
            if (responseData.redirect_url) {
                // If a redirect_url was provided, redirect to that URL
                window.location.href = responseData.redirect_url;
            }
        } else {
            alert('Sign In failed. Please check your credentials.');
        }
    }
    
    // Call sendData with handleSignInResponse as the callback
    sendData('/SignUsr', signInData, handleSignInResponse);



    function handleRegistrationResponse(responseData) {
        if (responseData.success) {
            alert('Registration successful');
        } else {
            alert('Registration failed. User already exists with this UID.');
        }
    }
});
