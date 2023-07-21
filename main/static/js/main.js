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


function toggleLanguage_client() {
    let toggleInput = document.querySelector(".toggle-input");
    let cat_today_headline = document.getElementById("cat_today_headline");
    let cat_other = document.getElementById("cat_other");
    let cat_sports = document.getElementById("cat_sports");
    let cat_showbiz = document.getElementById("cat_showbiz");
    let cat_world = document.getElementById("cat_world");
    let cat_country = document.getElementById("cat_country");
    let cat_national = document.getElementById("cat_national");

    let top_rolling_headline_bangla = document.querySelectorAll(".top_rolling_headline_bangla");
    let top_rolling_headline_english = document.querySelectorAll(".top_rolling_headline_english");

    let latest_news_title_bengali = document.querySelectorAll(".latest_news_title_bengali");
    let latest_news_title_english = document.querySelectorAll(".latest_news_title_english");

    let latest_news_title = document.getElementById("latest_news_title");

    if (toggleInput.checked) {
        cat_other.style.display = "block"
        cat_national.innerHTML = "জাতীয়";
        cat_country.innerHTML = "দেশগ্রাম";
        cat_world.innerHTML = "পূর্ব-পশ্চিম";
        cat_showbiz.innerHTML = "শোবিজ";
        cat_today_headline.innerHTML = "আজকের শিরোনাম";
        cat_sports.innerHTML = "মাঠে ময়দানে";

        top_rolling_headline_english.forEach(element => {
            element.style.display = "none";
        });
        top_rolling_headline_bangla.forEach(element => {
            element.style.display = "block";
        });

        latest_news_title_english.forEach(element => {
            element.style.display = "none";
        });
        latest_news_title_bengali.forEach(element => {
            element.style.display = "block";
        });

        latest_news_title.innerHTML = "সর্বশেষ খবর";

    } else {
        cat_other.style.display = "none"
        cat_national.innerHTML = "National";
        cat_country.innerHTML = "Country";
        cat_world.innerHTML = "World";
        cat_showbiz.innerHTML = "Showbiz";
        cat_today_headline.innerHTML = "Today's Headline";
        cat_sports.innerHTML = "Sports";

        top_rolling_headline_bangla.forEach(element => {
            element.style.display = "none";
        });
        top_rolling_headline_english.forEach(element => {
            element.style.display = "block";
        });

        latest_news_title_english.forEach(element => {
            element.style.display = "block";
        });
        latest_news_title_bengali.forEach(element => {
            element.style.display = "none";
        });

        latest_news_title.innerHTML = "Latest News";
    }
}