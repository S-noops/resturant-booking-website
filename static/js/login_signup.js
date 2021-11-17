const switchers = [...document.querySelectorAll('.switcher')]

switchers.forEach(item => {
	item.addEventListener('click', function() {
		switchers.forEach(item => item.parentElement.classList.remove('is-active'))
		this.parentElement.classList.add('is-active')
	})
})

sessionStorage.removeItem('email');

function login_error(){
    swal("Error!", "Login Credentials Incorrect!", "error");
}
function signup_error(){
    swal("Error!", "Duplicate Users Not Allowed!", "error");
}
function signup_success(){
    swal("Success!", "User Registration Done!", "success");
}

var login = document.getElementById("signIn");

// Handling the login of a user
login.addEventListener("submit", function(e){
    sessionStorage.setItem("email", document.getElementById("login-email").value);
    if (document.getElementById("login-email").value === ""){
        e.preventDefault();
    }
})

var signup = document.getElementById("signUp");

// Handling the submission of creation of a new user
signup.addEventListener("submit", function (e) {
    if (document.getElementById("signup-password").value !== document.getElementById("signup-password-confirm").value){
        e.preventDefault();
        detect();
    }
})

function detect() {
    document.getElementById("signup-password").classList.add("pass_mismatch");
    document.getElementById("signup-password-confirm").classList.add("pass_mismatch");
    document.getElementById("passHelp").style.display = "block";
}