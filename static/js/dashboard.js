// ==========================================
// AI Personality Dashboard
// dashboard.js
// ==========================================


// ==========================================
// Page Fade
// ==========================================

window.addEventListener("load", () => {

document.body.style.opacity="0";

setTimeout(()=>{

document.body.style.transition="opacity .8s ease";

document.body.style.opacity="1";

},100);

});


// ==========================================
// Navbar Scroll
// ==========================================

const navbar=document.querySelector(".dashboard-navbar");

window.addEventListener("scroll",()=>{

if(window.scrollY>40){

navbar.style.background="#08111F";

navbar.style.boxShadow="0 10px 30px rgba(0,0,0,.35)";

}

else{

navbar.style.background="rgba(8,17,31,.92)";

navbar.style.boxShadow="none";

}

});


// ==========================================
// Theme Toggle
// ==========================================

const themeBtn=document.getElementById("themeToggle");

const savedTheme=localStorage.getItem("theme");

if(savedTheme==="light"){

document.body.classList.add("light-mode");

themeBtn.innerHTML='<i class="bi bi-sun-fill"></i>';

}

if(themeBtn){

themeBtn.addEventListener("click",()=>{

document.body.classList.toggle("light-mode");

if(document.body.classList.contains("light-mode")){

localStorage.setItem("theme","light");

themeBtn.innerHTML='<i class="bi bi-sun-fill"></i>';

}

else{

localStorage.setItem("theme","dark");

themeBtn.innerHTML='<i class="bi bi-moon-fill"></i>';

}

});

}


// ==========================================
// Reveal Animation
// ==========================================

const reveal=document.querySelectorAll(

".trait-card,.analysis-box,.glass-card,.action-card"

);

const observer=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

entry.target.style.opacity="1";

entry.target.style.transform="translateY(0)";

}

});

},{threshold:.15});

reveal.forEach(card=>{

card.style.opacity="0";

card.style.transform="translateY(50px)";

card.style.transition=".8s";

observer.observe(card);

});
// ==========================================
// Progress Bar Animation
// ==========================================

const progressBars=document.querySelectorAll(".progress-bar");

const progressObserver=new IntersectionObserver(entries=>{

entries.forEach(entry=>{

if(entry.isIntersecting){

const bar=entry.target;

const width=bar.style.width;

bar.style.width="0%";

setTimeout(()=>{

bar.style.transition="width 2s ease";

bar.style.width=width;

},300);

}

});

},{threshold:.3});

progressBars.forEach(bar=>{

progressObserver.observe(bar);

});


// ==========================================
// Overall Score Counter
// ==========================================

const overall=document.querySelector(".analysis-box h1");

if(overall){

const finalValue=parseFloat(overall.innerText);

let current=0;

const counter=setInterval(()=>{

current+=0.05;

if(current>=finalValue){

current=finalValue;

clearInterval(counter);

}

overall.innerHTML=current.toFixed(2)+"/5";

},20);

}


// ==========================================
// Card Hover Effect
// ==========================================

const cards=document.querySelectorAll(

".trait-card,.analysis-box,.glass-card,.action-card"

);

cards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="translateY(-8px) scale(1.02)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="translateY(0) scale(1)";

});

});


// ==========================================
// Radar Chart
// ==========================================

const radarCanvas=document.getElementById("oceanChart");

if(radarCanvas){

new Chart(radarCanvas,{

type:"radar",

data:{

labels:[

"Openness",

"Conscientiousness",

"Extraversion",

"Agreeableness",

"Neuroticism"

],

datasets:[{

label:"OCEAN Score",

data:[

window.openness,

window.conscientiousness,

window.extraversion,

window.agreeableness,

window.neuroticism

],

fill:true,

backgroundColor:"rgba(108,99,255,.20)",

borderColor:"#6C63FF",

borderWidth:3,

pointBackgroundColor:"#ffffff",

pointBorderColor:"#6C63FF",

pointRadius:5

}]

},

options:{

responsive:true,

maintainAspectRatio:false,

scales:{

r:{

min:0,

max:5,

ticks:{

stepSize:1,

color:"#cbd5e1"

},

grid:{

color:"rgba(255,255,255,.15)"

},

angleLines:{

color:"rgba(255,255,255,.15)"

},

pointLabels:{

color:"#ffffff",

font:{

size:14,

weight:"bold"

}

}

}

},

plugins:{

legend:{

display:false

}

}

}

});

}


// ==========================================
// Console
// ==========================================

console.log("AI Dashboard Loaded Successfully 🚀");
