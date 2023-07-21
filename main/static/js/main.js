// Toggle Password
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

// Toggle Password End

// Image Upload
function readURL(input) {
    if (input.files && input.files[0]) {

        var reader = new FileReader();

        reader.onload = function (e) {
            $('.image-upload-wrap').hide();

            $('.file-upload-image').attr('src', e.target.result);
            $('.file-upload-content').show();

            $('.image-title').html(input.files[0].name);
        };

        // images validation
        const errorMessage = document.querySelector("#errorImage_4");
        const image = input.files[0];
        const {size, width} = image;
        console.log(size);
        if (size > 11000000) {
            errorMessage.textContent =
                "Image file is Larger than 10MB";
        } else {
            errorMessage.textContent = "";
            reader.readAsDataURL(input.files[0]);
        }
    } else {
        removeUpload();
    }
}

function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});

// Image Upload End

// DatePicker
