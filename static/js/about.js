// ========================================
// About Page JavaScript
// AI Personality Prediction System
// ========================================


// ================================
// Navbar Scroll Effect
// ================================

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


// ================================
// Page Load Animation
// ================================

window.addEventListener("load", () => {

    document.body.style.opacity = "0";

    setTimeout(() => {

        document.body.style.transition = "opacity .8s ease";

        document.body.style.opacity = "1";

    },100);

});


// ================================
// Scroll Reveal Animation
// ================================

const revealItems = document.querySelectorAll(

".about-section, .objectives-section, .work-card, .team-card, .flow-box, .cta-section"

);

const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.style.opacity="1";
            entry.target.style.transform="translateY(0)";

        }

    });

},{threshold:0.2});

revealItems.forEach(item=>{

    item.style.opacity="0";

    item.style.transform="translateY(40px)";

    item.style.transition="all .8s ease";

    observer.observe(item);

});


// ================================
// Hover Effect
// ================================

document.querySelectorAll(".work-card,.team-card,.flow-box").forEach(card=>{

    card.addEventListener("mouseenter",()=>{

        card.style.transform="translateY(-10px)";

    });

    card.addEventListener("mouseleave",()=>{

        card.style.transform="translateY(0px)";

    });

});


// ================================
// Console
// ================================

console.log("About Page Loaded Successfully 🚀");