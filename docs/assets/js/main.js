// Main JavaScript for Explosive Website Template

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initSmoothScrolling();
    initTableOfContents();
    initSearchFunctionality();
    initNewsletterForm();
    initContactForm();
});

// Mobile Menu Toggle
function initMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navigation = document.querySelector('.main-navigation');

    if (mobileToggle && navigation) {
        mobileToggle.addEventListener('click', function() {
            const isExpanded = mobileToggle.getAttribute('aria-expanded') === 'true';

            // Toggle aria-expanded attribute
            mobileToggle.setAttribute('aria-expanded', !isExpanded);

            // Toggle active classes
            mobileToggle.classList.toggle('active');
            navigation.classList.toggle('active');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileToggle.contains(e.target) && !navigation.contains(e.target)) {
                mobileToggle.setAttribute('aria-expanded', 'false');
                mobileToggle.classList.remove('active');
                navigation.classList.remove('active');
            }
        });

        // Close mobile menu when clicking on a nav link
        const navLinks = navigation.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileToggle.setAttribute('aria-expanded', 'false');
                mobileToggle.classList.remove('active');
                navigation.classList.remove('active');
            });
        });
    }
}

// Smooth Scrolling for Anchor Links
function initSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Table of Contents Generation
function initTableOfContents() {
    const tocContainer = document.getElementById('toc-container');
    const contentArea = document.querySelector('.post-content, .page-body, .content-wrapper');
    
    if (tocContainer && contentArea) {
        const headings = contentArea.querySelectorAll('h2, h3, h4, h5, h6');
        
        if (headings.length > 0) {
            const tocList = document.createElement('ul');
            tocList.className = 'toc-list';
            
            headings.forEach((heading, index) => {
                // Add ID to heading if it doesn't have one
                if (!heading.id) {
                    heading.id = `heading-${index}`;
                }
                
                const listItem = document.createElement('li');
                listItem.className = `toc-item toc-${heading.tagName.toLowerCase()}`;
                
                const link = document.createElement('a');
                link.href = `#${heading.id}`;
                link.textContent = heading.textContent;
                link.className = 'toc-link';
                
                listItem.appendChild(link);
                tocList.appendChild(listItem);
            });
            
            tocContainer.appendChild(tocList);
        } else {
            tocContainer.style.display = 'none';
        }
    }
}

// Search Functionality
function initSearchFunctionality() {
    const searchInput = document.querySelector('.search-input');
    const searchForm = document.querySelector('.search-form');
    
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            
            if (query) {
                // Simple search implementation - redirect to search page
                window.location.href = `/search/?q=${encodeURIComponent(query)}`;
            }
        });
    }
    
    // Collection page search
    const collectionSearchInput = document.getElementById('collection-search-input');
    if (collectionSearchInput) {
        let searchTimeout;
        
        collectionSearchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                filterPosts(this.value);
            }, 300);
        });
    }
}

// Filter posts in collection pages
function filterPosts(searchTerm) {
    const postCards = document.querySelectorAll('.post-card');
    const searchTermLower = searchTerm.toLowerCase();
    
    postCards.forEach(card => {
        const title = card.querySelector('.post-card-title')?.textContent.toLowerCase() || '';
        const description = card.querySelector('.post-card-description')?.textContent.toLowerCase() || '';
        const content = card.textContent.toLowerCase();
        
        const matches = title.includes(searchTermLower) || 
                       description.includes(searchTermLower) || 
                       content.includes(searchTermLower);
        
        card.style.display = matches ? 'block' : 'none';
    });
}

// Newsletter Form
function initNewsletterForm() {
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const submitButton = this.querySelector('button[type="submit"]');
            const email = emailInput.value.trim();
            
            if (email) {
                // Disable form during submission
                submitButton.disabled = true;
                submitButton.textContent = 'Subscribing...';
                
                // Simulate API call (replace with actual implementation)
                setTimeout(() => {
                    alert('Thank you for subscribing!');
                    emailInput.value = '';
                    submitButton.disabled = false;
                    submitButton.textContent = 'Subscribe';
                }, 1000);
            }
        });
    }
}

// Contact Form
function initContactForm() {
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitButton = this.querySelector('.submit-button');
            const formData = new FormData(this);
            
            // Basic validation
            const name = formData.get('name');
            const email = formData.get('email');
            const message = formData.get('message');
            
            if (!name || !email || !message) {
                alert('Please fill in all required fields.');
                return;
            }
            
            // Disable form during submission
            submitButton.disabled = true;
            submitButton.textContent = 'Sending...';
            
            // Simulate API call (replace with actual implementation)
            setTimeout(() => {
                alert('Thank you for your message! We\'ll get back to you soon.');
                this.reset();
                submitButton.disabled = false;
                submitButton.textContent = 'Send Message';
            }, 1000);
        });
    }
}

// Utility Functions

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Lazy loading for images
function initLazyLoading() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);
