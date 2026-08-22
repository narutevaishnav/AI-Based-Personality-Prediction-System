// ==========================================
// Analyze Page JavaScript
// AI Personality Prediction System
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ================= USERNAME VALIDATION =================

    const usernameForm = document.querySelector(
        'form input[name="username"]'
    );

    if (usernameForm) {

        usernameForm.addEventListener("input", function () {

            let value = this.value.trim();

            if (value.startsWith("@")) {

                this.value = value.substring(1);

            }

        });

    }

    // ================= POSTS COUNTER =================

    const textarea = document.querySelector(
        'textarea[name="posts"]'
    );

    if (textarea) {

        // Create Counter

        const counter = document.createElement("small");

        counter.style.color = "#94a3b8";

        counter.style.display = "block";

        counter.style.marginTop = "10px";

        counter.innerHTML = "Characters : 0";

        textarea.parentNode.appendChild(counter);

        textarea.addEventListener("input", function () {

            counter.innerHTML =
                "Characters : " + this.value.length;

        });

    }

    // ================= LOADING BUTTON =================

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const btn =
                form.querySelector("button");

            btn.disabled = true;

            btn.innerHTML =
                `<span class="spinner-border spinner-border-sm"></span>
                 Analyzing...`;

        });

    });

    // ================= CARD HOVER =================

    const cards =
        document.querySelectorAll(".analyze-card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform =
                "translateY(-10px) scale(1.02)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform =
                "translateY(0px) scale(1)";

        });

    });

});
// ================= IMAGE PREVIEW =================

const postImage = document.getElementById("postImage");
const previewBox = document.getElementById("previewBox");
const previewImage = document.getElementById("previewImage");
const removeImage = document.getElementById("removeImage");
const fileName = document.getElementById("fileName");

// ================= SELECT IMAGE =================

if (postImage) {

    postImage.addEventListener("change", function () {

        const file = this.files[0];

        if (file) {

            // Show File Name
            fileName.innerHTML = file.name;

            // Preview Image
            const reader = new FileReader();

            reader.onload = function (e) {

                previewImage.src = e.target.result;

                previewBox.style.display = "block";

            };

            reader.readAsDataURL(file);

        }

    });

}

// ================= REMOVE IMAGE =================

if (removeImage) {

    removeImage.addEventListener("click", function () {

        postImage.value = "";

        previewImage.src = "";

        previewBox.style.display = "none";

        fileName.innerHTML = "No image selected";

    });

}
// ================= LIGHTBOX =================

const lightbox = document.getElementById("imageLightbox");
const lightboxImage = document.getElementById("lightboxImage");
const closeLightbox = document.getElementById("closeLightbox");

// Open

previewImage.addEventListener("click", function () {

    if (previewImage.src !== "") {

        lightbox.style.display = "flex";

        lightboxImage.src = previewImage.src;

    }

});

// Close Button

closeLightbox.addEventListener("click", function () {

    lightbox.style.display = "none";

});

// Close on Background Click

lightbox.addEventListener("click", function (e) {

    if (e.target === lightbox) {

        lightbox.style.display = "none";

    }

});
