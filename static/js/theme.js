// ==========================================
// Common Theme JavaScript
// AI Personality Prediction System
// ==========================================


// ================================
// Load Saved Theme
// ================================

window.addEventListener("load", function () {

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {

        document.body.classList.add("light-mode");

    }

    updateThemeIcon();

});


// ================================
// Theme Toggle
// ================================

function toggleTheme() {

    document.body.classList.toggle("light-mode");

    if (document.body.classList.contains("light-mode")) {

        localStorage.setItem("theme", "light");

    } else {

        localStorage.setItem("theme", "dark");

    }

    updateThemeIcon();

}


// ================================
// Change Button Icon
// ================================

function updateThemeIcon() {

    const icon = document.getElementById("themeIcon");

    if (!icon) return;

    if (document.body.classList.contains("light-mode")) {

        icon.className = "bi bi-sun-fill";

    } else {

        icon.className = "bi bi-moon-fill";

    }

}