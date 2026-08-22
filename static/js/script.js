// =========================================
// AI Personality Prediction System
// script.js
// =========================================


// -------------------------------
// Navbar Scroll Effect
// -------------------------------

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (window.scrollY > 50) {

        navbar.style.background = "#08111F";
        navbar.style.boxShadow = "0 8px 25px rgba(0,0,0,.4)";

    } else {

        navbar.style.background = "rgba(8,17,31,.85)";
        navbar.style.boxShadow = "none";

    }

});


// -------------------------------
// Hero Animation
// -------------------------------

window.addEventListener("load", function () {

    const hero = document.querySelector(".hero");

    hero.style.opacity = "0";
    hero.style.transform = "translateY(30px)";

    setTimeout(() => {

        hero.style.transition = "all 1s ease";

        hero.style.opacity = "1";
        hero.style.transform = "translateY(0)";

    }, 200);

});


// -------------------------------
// Button Hover Animation
// -------------------------------

document.querySelectorAll(".btn").forEach(btn => {

    btn.addEventListener("mouseenter", function () {

        btn.style.transform = "translateY(-4px)";

    });

    btn.addEventListener("mouseleave", function () {

        btn.style.transform = "translateY(0)";

    });

});


// -------------------------------
// Counter Animation
// -------------------------------

const counters = document.querySelectorAll(".stat-card h2");

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            const counter = entry.target;

            const text = counter.textContent.trim();

            const number = parseInt(text.replace(/\D/g, ""));

            if (isNaN(number)) return;

            const suffix = text.includes("%") ? "%" : "+";

            let current = 0;

            const increment = Math.ceil(number / 50);

            const timer = setInterval(() => {

                current += increment;

                if (current >= number) {

                    current = number;

                    clearInterval(timer);

                }

                counter.textContent = current + suffix;

            }, 30);

            observer.unobserve(counter);

        }

    });

}, {

    threshold: 0.5

});

counters.forEach(counter => {

    observer.observe(counter);

});


// -------------------------------
// Scroll Reveal Animation
// -------------------------------

const revealElements = document.querySelectorAll(

    ".stat-card, .work-card, .about-preview"

);

const revealObserver = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";

        }

    });

}, {

    threshold: 0.2

});

revealElements.forEach(item => {

    item.style.opacity = "0";
    item.style.transform = "translateY(40px)";
    item.style.transition = "all .8s ease";

    revealObserver.observe(item);

});


// -------------------------------
// Console
// -------------------------------

console.log("AI Personality Prediction System Loaded Successfully 🚀");