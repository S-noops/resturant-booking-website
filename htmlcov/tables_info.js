function getCurrentMonth(){
    let dateObj = new Date();
    let myDate = (dateObj.getUTCFullYear()) + "-" + (dateObj.getMonth() + 2);
    return myDate;
}

document.getElementById("card_expiry").min= getCurrentMonth(); 
document.getElementById("card_expiry_signup").min= getCurrentMonth(); 

function ValidateCreditCardNumber(val) {
    var ccNum = val;
    var visaRegEx = /^(?:4[0-9]{12}(?:[0-9]{3})?)$/;
    var mastercardRegEx = /^(?:5[1-5][0-9]{14})$/;
    var amexpRegEx = /^(?:3[47][0-9]{13})$/;
    var discovRegEx = /^(?:6(?:011|5[0-9][0-9])[0-9]{12})$/;
    var isValid = false;

    if (visaRegEx.test(ccNum)) {
        isValid = true;
    } else if(mastercardRegEx.test(ccNum)) {
        isValid = true;
    } else if(amexpRegEx.test(ccNum)) {
        isValid = true;
    } else if(discovRegEx.test(ccNum)) {
        isValid = true;
    }

    return isValid;
}

var dir_form = document.getElementById("validate");

dir_form.addEventListener("submit", function(e){
    if (ValidateCreditCardNumber(document.getElementById("card_no").value)=== false){
        swal("Error!", "Card Number Incorrect!", "error");
        e.preventDefault();
    }
});

var signup = document.getElementById("signUp");

// Handling the submission of creation of a new user
signup.addEventListener("submit", function (e) {
    sessionStorage.setItem("email", document.getElementById("signup-email").value);
    if (document.getElementById("signup-password").value !== document.getElementById("signup-password-confirm").value){
        swal("Error!", "Passwords Don't match!", "error");
        e.preventDefault();
    }
    if (ValidateCreditCardNumber(document.getElementById("card_no_signup").value)=== false){
        swal("Error!", "Card Number Incorrect!", "error");
        e.preventDefault();
    }
})
