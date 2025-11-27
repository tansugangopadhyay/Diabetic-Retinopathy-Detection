// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadContent = document.getElementById('uploadContent');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const removeBtn = document.getElementById('removeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const analyzeBtnText = document.getElementById('analyzeBtnText');
const spinner = document.getElementById('spinner');
const resultsContainer = document.getElementById('resultsContainer');

// State
let selectedFile = null;

// Color mapping for severity levels
const severityColors = {
    0: '#10b981', // No DR - Green
    1: '#3b82f6', // Mild - Blue
    2: '#f59e0b', // Moderate - Orange
    3: '#ef4444', // Severe - Red
    4: '#dc2626'  // Proliferative DR - Dark Red
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkAPIHealth();
});

// Event Listeners
function initializeEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', () => {
        if (!selectedFile) {
            fileInput.click();
        }
    });

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Remove button
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        removeFile();
    });

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeImage);

    // Smooth scroll for navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            scrollToSection(targetId);
            
            // Update active state
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        });
    });
}

// File handling
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        validateAndDisplayFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const file = e.dataTransfer.files[0];
    if (file) {
        validateAndDisplayFile(file);
    }
}

function validateAndDisplayFile(file) {
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
        showNotification('Please upload a PNG, JPG, or JPEG image.', 'error');
        return;
    }

    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showNotification('File size must be less than 16MB.', 'error');
        return;
    }

    selectedFile = file;
    displayPreview(file);
    analyzeBtn.disabled = false;
    resultsContainer.style.display = 'none';
}

function displayPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadContent.style.display = 'none';
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    previewImage.src = '';
    uploadContent.style.display = 'block';
    previewContainer.style.display = 'none';
    analyzeBtn.disabled = true;
    resultsContainer.style.display = 'none';
}

// API Functions
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (!data.model_loaded) {
            showNotification('Model not loaded. Please check the backend configuration.', 'warning');
        }
    } catch (error) {
        console.error('API health check failed:', error);
        showNotification('Unable to connect to the backend server. Please ensure it is running.', 'error');
    }
}

async function analyzeImage() {
    if (!selectedFile) return;

    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtnText.textContent = 'Analyzing...';
    spinner.style.display = 'block';

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }

        const result = await response.json();
        displayResults(result);
        
        // Scroll to results
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 300);

    } catch (error) {
        console.error('Analysis error:', error);
        showNotification(error.message || 'Failed to analyze image. Please try again.', 'error');
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        analyzeBtnText.textContent = 'Analyze Image';
        spinner.style.display = 'none';
    }
}

// Display Results
function displayResults(result) {
    const { severity_value, severity_class, confidence, probabilities, info } = result;

    // Show results container
    resultsContainer.style.display = 'block';

    // Update result badge
    const resultBadge = document.getElementById('resultBadge');
    resultBadge.textContent = severity_class;
    resultBadge.style.background = severityColors[severity_value];

    // Update severity indicator (circular progress)
    updateCircularProgress(confidence, severityColors[severity_value]);
    document.getElementById('severityValue').textContent = `${confidence}%`;

    // Update result details
    document.getElementById('diagnosisValue').textContent = severity_class;
    document.getElementById('diagnosisValue').style.color = severityColors[severity_value];
    
    document.getElementById('riskValue').textContent = info.risk;
    document.getElementById('riskValue').style.color = severityColors[severity_value];
    
    document.getElementById('descriptionValue').textContent = info.description;
    document.getElementById('recommendationValue').textContent = info.recommendation;

    // Update probability bars
    displayProbabilityBars(probabilities);
}

function updateCircularProgress(percentage, color) {
    const circle = document.getElementById('progressCircle');
    const radius = 90;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (percentage / 100) * circumference;

    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = circumference;
    circle.style.stroke = color;

    // Animate
    setTimeout(() => {
        circle.style.strokeDashoffset = offset;
    }, 100);
}

function displayProbabilityBars(probabilities) {
    const container = document.getElementById('probabilityBars');
    container.innerHTML = '';

    const classes = ['No DR', 'Mild', 'Moderate', 'Severe', 'Proliferative DR'];
    const colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#dc2626'];

    classes.forEach((className, index) => {
        const probability = probabilities[className] || 0;
        
        const barElement = document.createElement('div');
        barElement.className = 'probability-bar';
        barElement.innerHTML = `
            <div class="probability-label">${className}</div>
            <div class="probability-track">
                <div class="probability-fill" style="width: 0%; background: ${colors[index]};"></div>
            </div>
            <div class="probability-value">${probability.toFixed(1)}%</div>
        `;
        
        container.appendChild(barElement);

        // Animate bar
        setTimeout(() => {
            const fill = barElement.querySelector('.probability-fill');
            fill.style.width = `${probability}%`;
        }, 100 + (index * 50));
    });
}

// Utility Functions
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const navHeight = document.querySelector('.navbar').offsetHeight;
        const sectionTop = section.offsetTop - navHeight - 20;
        window.scrollTo({
            top: sectionTop,
            behavior: 'smooth'
        });
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-icon">
                ${type === 'error' ? '⚠️' : type === 'warning' ? '⚡' : 'ℹ️'}
            </span>
            <span class="notification-message">${message}</span>
        </div>
    `;

    // Add styles if not already present
    if (!document.getElementById('notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 100px;
                right: 20px;
                max-width: 400px;
                padding: 1rem 1.5rem;
                background: rgba(15, 23, 42, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 1rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
                z-index: 10000;
                animation: slideIn 0.3s ease;
            }
            
            .notification-error {
                border-left: 4px solid #ef4444;
            }
            
            .notification-warning {
                border-left: 4px solid #f59e0b;
            }
            
            .notification-info {
                border-left: 4px solid #3b82f6;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                color: white;
            }
            
            .notification-icon {
                font-size: 1.25rem;
            }
            
            .notification-message {
                flex: 1;
                font-size: 0.875rem;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(400px);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// Scroll-based navigation highlighting
let scrollTimeout;
window.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        const sections = ['home', 'about', 'detection', 'info'];
        const navHeight = document.querySelector('.navbar').offsetHeight;
        
        let currentSection = 'home';
        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            if (section) {
                const rect = section.getBoundingClientRect();
                if (rect.top <= navHeight + 100 && rect.bottom >= navHeight) {
                    currentSection = sectionId;
                }
            }
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }, 100);
});

// Add smooth scroll polyfill for older browsers
if (!('scrollBehavior' in document.documentElement.style)) {
    const style = document.createElement('style');
    style.textContent = `
        * {
            scroll-behavior: auto !important;
        }
    `;
    document.head.appendChild(style);
}

console.log('🚀 Diabetic Retinopathy Detection System Initialized');
console.log('📡 API Base URL:', API_BASE_URL);
