// Dark Mode Toggle Functionality
(function() {
    'use strict';
    
    // Get saved theme from localStorage or default to 'light'
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Apply theme on page load
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Create toggle button
    function createToggleButton() {
        const button = document.createElement('button');
        button.className = 'theme-toggle';
        button.setAttribute('aria-label', 'Toggle dark mode');
        button.setAttribute('title', 'Toggle dark/light mode');
        
        // Set initial icon based on current theme
        updateButtonIcon(button, savedTheme);
        
        // Add click event
        button.addEventListener('click', toggleTheme);
        
        // Add to body
        document.body.appendChild(button);
        
        return button;
    }
    
    // Update button icon
    function updateButtonIcon(button, theme) {
        if (theme === 'dark') {
            button.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            button.innerHTML = '<i class="fas fa-moon"></i>';
        }
    }
    
    // Toggle theme
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Apply new theme
        document.documentElement.setAttribute('data-theme', newTheme);
        
        // Save to localStorage
        localStorage.setItem('theme', newTheme);
        
        // Update button icon
        const button = document.querySelector('.theme-toggle');
        updateButtonIcon(button, newTheme);
        
        // Optional: Add animation effect
        button.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            button.style.transform = '';
        }, 300);
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createToggleButton);
    } else {
        createToggleButton();
    }
})();
