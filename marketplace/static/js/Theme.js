
window.onload = () => {
    console.log('Market loaded');
    
    // Get saved theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');

    // Apply saved theme or default to light
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        themeIcon.className = 'bi bi-moon-fill';
    } else {
        body.classList.remove('dark-theme');
        themeIcon.className = 'bi bi-sun-fill';
    }

    // Initialize theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
};

window.addEventListener('load', () => {
    console.log('Handler 1: loaded!');
});
window.addEventListener('load', () => {
    console.log('Handler 2: Welcome to the Marketplace!');
    
    // Check if user is visiting for the first time
    if (!localStorage.getItem('visited')) {
        console.log('First time visitor detected');
        localStorage.setItem('visited', 'true');
        // Could add first-time visitor specific actions here
    }

    // Check if marketplace items are loaded
    const marketItems = document.querySelector('.market-items');
    if (marketItems) {
        console.log('Market items container found');
    } else {
        console.warn('Market items container not found');
    }

    // Initialize any marketplace specific features
    initializeMarketplace();
});

function initializeMarketplace() {
    // Add any marketplace initialization logic here
    console.log('Marketplace initialized');
}

// Toggle theme Function
function toggleTheme() {
    const body = document.body;
    const icon = document.getElementById('theme-icon');

    body.classList.toggle('dark-theme');
    if (body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
        icon.className = 'bi bi-moon-fill';
    }else {
        localStorage.setItem('theme', 'light');
        icon.className = 'bi bi-sun-fill';
    }
}