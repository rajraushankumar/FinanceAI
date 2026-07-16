const togglePassword = document.getElementById("togglePassword");
const password = document.getElementById("password");

togglePassword.addEventListener("click", function(){

    if(password.type === "password"){

        password.type = "text";

        togglePassword.classList.remove("fa-eye");
        togglePassword.classList.add("fa-eye-slash");

    }else{

        password.type = "password";

        togglePassword.classList.remove("fa-eye-slash");
        togglePassword.classList.add("fa-eye");

    }

});

const loginForm = document.getElementById("loginForm");
const loginBtn = document.getElementById("loginBtn");

loginForm.addEventListener("submit", function(){

    loginBtn.disabled = true;

    loginBtn.innerHTML = `
        <i class="fa-solid fa-spinner fa-spin"></i>
        Logging in...
    `;

});