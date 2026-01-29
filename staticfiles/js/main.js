const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;

themeToggle.addEventListener('click', () => {
    if (html.getAttribute('data-bs-theme') === 'light') {
        html.setAttribute('data-bs-theme', 'dark');
        themeToggle.textContent = '☀️';
    } else {
        html.setAttribute('data-bs-theme', 'light');
        themeToggle.textContent = '🌙';
    }
});
