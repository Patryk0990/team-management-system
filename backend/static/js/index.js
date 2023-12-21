let registerForm = document.getElementById("register-form");
let loginForm = document.getElementById("login-form");
let forms = document.getElementsByClassName("forms")[0];

function changeFormDisplay() {

    if (loginForm.classList.contains("active")) {
        if (window.innerWidth >= 768) {
            forms.style.left = "-50vw";
        }
        else {
            forms.style.left = "-100vw";
        }
        setTimeout(() => {
            forms.style.display = "none";
            forms.style.left = "100vw";
            if (window.innerWidth >= 768) {
                forms.style.clipPath = "polygon(10% 0, 100% 0, 100% 100%, 0 100%)";
            }
            loginForm.classList.remove("active");
            registerForm.classList.add("active");
            setTimeout(() => {
                forms.style.display = "flex";
                setTimeout(() => {
                    if (window.innerWidth >= 768) {
                        forms.style.left = "50vw";
                    }
                    else {
                        forms.style.left = "0";
                    }
                }, 75)
            }, 75)
        }, 150)
    }
    else {
        forms.style.left = "100vw";
        setTimeout(() => {
            forms.style.display = "none";
            if (window.innerWidth >= 768) {
                forms.style.left = "-50vw";
                forms.style.clipPath = "polygon(0 0, 100% 0, 90% 100%, 0% 100%)";
            }
            else {
                forms.style.left = "-100vw";
            }
            registerForm.classList.remove("active");
            loginForm.classList.add("active");
            setTimeout(() => {
                forms.style.display = "flex";
                setTimeout(() => {
                    forms.style.left = "0";
                }, 75)
            }, 75)
        }, 150)
    }
}

function initFormDisplay() {

    if (registerForm.classList.contains("active") && window.innerWidth >= 768) {
        forms.style.clipPath = "polygon(10% 0, 100% 0, 100% 100%, 0 100%)";
        forms.style.left = "50vw";
    }
    forms.style.display = "flex";
}

window.addEventListener("load", initFormDisplay);