function passwordShow() {
  let passwordInput = document.getElementById("passwordInput");
  let togglePassword = document.getElementById("togglePassword_1");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    togglePassword.classList.remove("bi-eye-slash");
    togglePassword.classList.add("bi-eye");
  } else {
    passwordInput.type = "password";
    togglePassword.classList.remove("bi-eye");
    togglePassword.classList.add("bi-eye-slash");
  }
}
