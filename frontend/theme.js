// Theme Management
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update icon
    const icon = document.querySelector('.theme-icon');
    icon.textContent = newTheme === 'dark' ? '🌙' : '☀️';
    
    // Reload charts with new theme
    setTimeout(() => {
        loadAllVisualizations();
    }, 100);
}

function setAccent(color) {
    const html = document.documentElement;
    html.setAttribute('data-accent', color);
    localStorage.setItem('accent', color);
    
    // Update active state
    document.querySelectorAll('.accent-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-accent="${color}"]`).classList.add('active');
    
    // Reload charts with new accent
    setTimeout(() => {
        loadAllVisualizations();
    }, 100);
}

// Load saved preferences
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const savedAccent = localStorage.getItem('accent') || 'purple';
    
    document.documentElement.setAttribute('data-theme', savedTheme);
    document.documentElement.setAttribute('data-accent', savedAccent);
    
    // Update icon
    const icon = document.querySelector('.theme-icon');
    if (icon) {
        icon.textContent = savedTheme === 'dark' ? '🌙' : '☀️';
    }
    
    // Update active accent button
    const accentBtn = document.querySelector(`[data-accent="${savedAccent}"]`);
    if (accentBtn) {
        accentBtn.classList.add('active');
    }
});
