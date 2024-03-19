var mouseclick = new Audio();
mouseclick.src = "https://uploads.sitepoint.com/wp-content/uploads/2023/06/1687569402mixkit-fast-double-click-on-mouse-275.wav";

// script.js


//  loader animation
window.onload = function() {
    // Simulate an API request or any async operation
    setTimeout(() => {
        hideLoader();
        showContent();
    }, 1000); // Replace with your actual data loading logic and time

};


function hideLoader() {
    const loader = document.getElementById("loader");
    loader.style.display = "none";
}

function showContent() {
    const content = document.getElementById("content");
    content.style.display = "block";
}

function showLoader() {
    const loader = document.getElementById("loader");
    loader.style.display = "block";
}

function hideContent() {
    const content = document.getElementById("content");
    content.style.display = "none";
}