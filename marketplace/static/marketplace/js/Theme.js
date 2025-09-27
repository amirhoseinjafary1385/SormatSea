window.onload = () => {
    console.log('Market loaded');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        document.getElementById('theme-icon').className = 'bi bi-moon-fill';
    } else {
        document.getElementById('theme-icon').className = 'bi bi-sun-fill';
    }
};


window.addEventListener('load', () => {
    console.log('Handler 1: loaded!');
    //alert('Welcome to the SormatSea.io!');
});

window.addEventListener('load', () => {
    console.log('Handler 2: Welcome to the Marketplace!');
});

// Toggle theme Function
function toggleTheme() {
    const body = document.body;
    const icon = document.getElementById('theme-icon');
    
    body.classList.toggle('dark-theme');
    if (body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
        icon.className = 'bi bi-moon-fill';
    } else {
        localStorage.setItem('theme', 'light');
        icon.className = 'bi bi-sun-fill';
    }
}