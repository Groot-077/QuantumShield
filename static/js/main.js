/**
 * QuantumShield Client-Side JavaScript Engine
 * Provides theme toggling (Light/Dark mode), live password strength estimation, clipboard copying, and UI animations.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Theme Switcher
    initThemeToggle();

    // 2. Password Strength Meter Listener
    const passwordInput = document.getElementById('password');
    const strengthBar = document.getElementById('strength-bar');
    const strengthText = document.getElementById('strength-text');

    if (passwordInput && strengthBar && strengthText) {
        passwordInput.addEventListener('input', () => {
            const val = passwordInput.value;
            const score = calculatePasswordStrength(val);
            updateStrengthMeter(score, strengthBar, strengthText);
        });
    }

    // 3. Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 6000);
    });
});

/**
 * Manages Theme Toggle (Light <-> Dark Mode) with LocalStorage persistence
 */
function initThemeToggle() {
    const toggleBtn = document.getElementById('theme-toggle-btn');
    const themeIcon = document.getElementById('theme-icon');

    // Fetch saved theme preference or default to light
    const currentTheme = localStorage.getItem('quantumshield_theme') || 'light';
    applyTheme(currentTheme, themeIcon);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = activeTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('quantumshield_theme', newTheme);
            updateThemeIcon(newTheme, themeIcon);
        });
    }
}

function applyTheme(theme, iconElement) {
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    updateThemeIcon(theme, iconElement);
}

function updateThemeIcon(theme, iconElement) {
    if (!iconElement) return;
    if (theme === 'dark') {
        iconElement.className = 'fa-solid fa-sun text-warning';
    } else {
        iconElement.className = 'fa-solid fa-moon text-primary';
    }
}

/**
 * Calculates Password Complexity Score (0 to 4)
 */
function calculatePasswordStrength(password) {
    if (!password) return 0;
    let score = 0;
    
    if (password.length >= 8) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (/[0-9]/.test(password) && /[^A-Za-z0-9]/.test(password)) score += 1;

    return score;
}

/**
 * Updates UI Strength Meter Bar
 */
function updateStrengthMeter(score, meterBar, meterText) {
    meterBar.className = 'strength-meter-bar';

    switch (score) {
        case 0:
            meterText.textContent = '';
            meterBar.style.width = '0%';
            break;
        case 1:
            meterBar.classList.add('strength-weak');
            meterText.textContent = 'Weak (Add length & special characters)';
            meterText.className = 'text-danger small mt-1';
            break;
        case 2:
            meterBar.classList.add('strength-fair');
            meterText.textContent = 'Fair (Add uppercase & numbers)';
            meterText.className = 'text-warning small mt-1';
            break;
        case 3:
            meterBar.classList.add('strength-good');
            meterText.textContent = 'Good Password';
            meterText.className = 'text-info small mt-1';
            break;
        case 4:
            meterBar.classList.add('strength-strong');
            meterText.textContent = 'Strong Post-Quantum Password';
            meterText.className = 'text-success small mt-1';
            break;
    }
}

/**
 * Helper to copy PQC Key text to clipboard
 */
function copyToClipboard(elementId) {
    const textElement = document.getElementById(elementId);
    if (textElement) {
        navigator.clipboard.writeText(textElement.innerText).then(() => {
            alert('PQC Key copied to clipboard!');
        }).catch(err => {
            console.error('Copy failed', err);
        });
    }
}
