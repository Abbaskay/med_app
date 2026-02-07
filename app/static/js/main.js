document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current navigation item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Initialize tooltips if any
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        // Simple tooltip implementation
        tooltip.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltipEl = document.createElement('div');
            tooltipEl.className = 'tooltip';
            tooltipEl.textContent = tooltipText;
            document.body.appendChild(tooltipEl);
            
            const rect = this.getBoundingClientRect();
            tooltipEl.style.top = `${rect.top - tooltipEl.offsetHeight - 10}px`;
            tooltipEl.style.left = `${rect.left + (rect.width / 2) - (tooltipEl.offsetWidth / 2)}px`;
            tooltipEl.style.opacity = '1';
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltipEl = document.querySelector('.tooltip');
            if (tooltipEl) {
                tooltipEl.remove();
            }
        });
    });
    
    // Handle probability bar animation
    const probabilityBars = document.querySelectorAll('.probability-fill');
    probabilityBars.forEach(bar => {
        const percentage = bar.getAttribute('data-percentage');
        setTimeout(() => {
            bar.style.width = `${percentage}%`;
        }, 100);
    });
    
    // Initialize charts if they exist on the page
    if (typeof Chart !== 'undefined') {
        const healthCharts = document.querySelectorAll('[data-chart]');
        
        healthCharts.forEach(chartCanvas => {
            const chartType = chartCanvas.getAttribute('data-chart');
            
            if (chartType === 'risk-factors') {
                const ctx = chartCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Age', 'Blood Pressure', 'Cholesterol', 'BMI', 'Glucose', 'Smoking'],
                        datasets: [{
                            label: 'Impact on Risk',
                            data: [65, 75, 80, 60, 70, 85],
                            backgroundColor: [
                                'rgba(78, 165, 217, 0.7)',
                                'rgba(100, 201, 160, 0.7)',
                                'rgba(248, 169, 120, 0.7)',
                                'rgba(78, 165, 217, 0.7)',
                                'rgba(100, 201, 160, 0.7)',
                                'rgba(248, 169, 120, 0.7)'
                            ],
                            borderColor: [
                                'rgba(78, 165, 217, 1)',
                                'rgba(100, 201, 160, 1)',
                                'rgba(248, 169, 120, 1)',
                                'rgba(78, 165, 217, 1)',
                                'rgba(100, 201, 160, 1)',
                                'rgba(248, 169, 120, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        },
                        plugins: {
                            legend: {
                                display: false
                            }
                        }
                    }
                });
            }
            
            if (chartType === 'prediction-trends') {
                const ctx = chartCanvas.getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['20-30', '30-40', '40-50', '50-60', '60-70', '70-80'],
                        datasets: [
                            {
                                label: 'Heart Disease Risk by Age',
                                data: [5, 12, 25, 40, 55, 65],
                                borderColor: 'rgba(78, 165, 217, 1)',
                                backgroundColor: 'rgba(78, 165, 217, 0.1)',
                                fill: true,
                                tension: 0.4
                            },
                            {
                                label: 'Diabetes Risk by Age',
                                data: [3, 15, 30, 45, 50, 52],
                                borderColor: 'rgba(100, 201, 160, 1)',
                                backgroundColor: 'rgba(100, 201, 160, 0.1)',
                                fill: true,
                                tension: 0.4
                            }
                        ]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100,
                                title: {
                                    display: true,
                                    text: 'Risk Percentage'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Age Groups'
                                }
                            }
                        }
                    }
                });
            }
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    
                    // Add error message if doesn't exist
                    let errorMessage = field.parentNode.querySelector('.form-error');
                    if (!errorMessage) {
                        errorMessage = document.createElement('div');
                        errorMessage.className = 'form-error';
                        errorMessage.textContent = 'This field is required';
                        field.parentNode.appendChild(errorMessage);
                    }
                    
                    // Add error styling
                    field.style.borderColor = 'var(--error)';
                } else {
                    // Remove error styling and message
                    field.style.borderColor = '';
                    const errorMessage = field.parentNode.querySelector('.form-error');
                    if (errorMessage) {
                        errorMessage.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });
});

// Theme toggle functionality
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateThemeToggleButton(theme);
}

function updateThemeToggleButton(theme) {
    const button = document.getElementById('theme-toggle');
    if (button) {
        const icon = theme === 'dark' ? '☀️' : '🌙';
        const text = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
        button.innerHTML = `${icon} ${text}`;
    }
}

// Initialize theme
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    // Add click event listener to theme toggle button
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }
}); 