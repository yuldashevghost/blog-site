// script.js

// Select the burger menu icon and navigation links
const burgerMenu = document.querySelector('.burger-menu');
const navLinks = document.querySelector('.nav-links');

// Toggle the 'active' class on the navigation links when the burger menu is clicked
burgerMenu.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Close the navigation menu when a link is clicked (for better user experience on mobile)
const navItems = document.querySelectorAll('.nav-links li a');

navItems.forEach(item => {
    item.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});
