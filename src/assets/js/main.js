// Main JavaScript for Explosive Website Template

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initSmoothScrolling();
    initTableOfContents();
    initSearchFunctionality();
    initNewsletterForm();
    initContactForm();
    initTabs();
    initProjectPreview();
});

// Accessible tabs initialization
function initTabs() {
    const tablists = document.querySelectorAll('[role="tablist"], .tablist, .tab-buttons');
    tablists.forEach(list => {
        // support both ARIA tablist (.tablist/.tab) and simple .tab-buttons/.tab-pane structures
        const tabs = Array.from(list.querySelectorAll('[role="tab"], .tab, .tab-button'));
        
        // Initialize active class based on aria-selected state
        tabs.forEach(tab => {
            if (tab.classList.contains('tab-button') && tab.getAttribute('aria-selected') === 'true') {
                tab.classList.add('active');
            }
        });
        
        tabs.forEach((tab, idx) => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                activateTab(tab, tabs);
            });
            tab.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    const next = tabs[(idx + 1) % tabs.length];
                    next.focus();
                    activateTab(next, tabs);
                } else if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    const prev = tabs[(idx - 1 + tabs.length) % tabs.length];
                    prev.focus();
                    activateTab(prev, tabs);
                }
            });
        });
    });

    // Activate tab from hash on load
    const hash = window.location.hash.slice(1);
    if (hash) {
        // Try modern ARIA tab id, then legacy data-tab setup
        let targetTab = document.querySelector(`[data-tab-id="${hash}"]`);
        if (!targetTab) targetTab = document.querySelector(`.tab-button[data-tab="${hash}"]`);
        if (targetTab) {
            const root = targetTab.closest('[role="tablist"], .tablist, .tab-buttons');
            const allTabs = Array.from(root.querySelectorAll('[role="tab"], .tab, .tab-button'));
            activateTab(targetTab, allTabs);
            
            // Scroll to the section containing this tab
            const section = targetTab.closest('.custom-section');
            if (section) {
                // Use setTimeout to ensure DOM is fully rendered before scrolling
                setTimeout(() => {
                    section.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 100);
            }
        }
    }

    // Handle sidebar links that point to tabs
    const sidebarLinks = document.querySelectorAll('.nav-link[data-tab-link]');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const tabId = link.dataset.tabLink;
            const targetTab = document.querySelector(`.tab-button[data-tab="${tabId}"]`);
            if (targetTab) {
                // If we are on the home page, prevent default and switch tab
                // Check for home page by looking at pathname end (works with any path prefix)
                const pathname = window.location.pathname;
                const isHomePage = pathname === '/' || pathname.endsWith('/index.html') || pathname.endsWith('/');
                if (isHomePage) {
                    e.preventDefault(); // Prevent default navigation to update hash manually
                    const root = targetTab.closest('[role="tablist"], .tablist, .tab-buttons');
                    const allTabs = Array.from(root.querySelectorAll('[role="tab"], .tab, .tab-button'));
                    activateTab(targetTab, allTabs);
                    
                    // Scroll to the section container (not the tab button itself)
                    const section = targetTab.closest('.custom-section');
                    if (section) {
                        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            }
        });
    });
}

function activateTab(tab, tabs) {
    // Handle ARIA tabs and simple tab-buttons
    tabs.forEach(t => {
        // reset selection for accessible tabs
        if (t.matches('[role="tab"]') || t.classList.contains('tab')) {
            t.setAttribute('aria-selected', 'false');
        }
        // Also handle active class for tab-buttons (can have both role="tab" and class="tab-button")
        if (t.classList.contains('tab-button')) {
            t.classList.remove('active');
        }

        const panelId = t.getAttribute('aria-controls') || t.dataset.controls || t.dataset.tab;
        if (panelId) {
            const panel = document.getElementById(panelId);
            if (panel) panel.setAttribute('aria-hidden', 'true');
            if (panel && panel.classList.contains('tab-pane')) panel.classList.remove('active');
        }
    });

    // activate selected
    if (tab.matches('[role="tab"]') || tab.classList.contains('tab')) {
        tab.setAttribute('aria-selected', 'true');
    }
    // Also handle active class for tab-buttons (can have both role="tab" and class="tab-button")
    if (tab.classList.contains('tab-button')) {
        tab.classList.add('active');
    }

    const panelId = tab.getAttribute('aria-controls') || tab.dataset.controls || tab.dataset.tab;
    if (panelId) {
        const panel = document.getElementById(panelId);
        if (panel) {
            panel.setAttribute('aria-hidden', 'false');
            if (panel.classList.contains('tab-pane')) panel.classList.add('active');
        }
    }

    // Update hash for deep-linking (use tab.dataset.tab or explicit id)
    const tabId = tab.dataset.tabId || tab.dataset.tab || panelId;
    if (tabId) {
        history.replaceState(null, '', `#${tabId}`);
    }
}

// Project preview wiring: populate the right-column project-detail when a project card is clicked
function initProjectPreview() {
    const postCards = document.querySelectorAll('.post-card, .project-card');
    const detail = document.getElementById('project-detail');
    if (!detail) return;

    postCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', (e) => {
            // extract simple fields
            const title = card.querySelector('.post-card-title a')?.textContent || card.querySelector('.post-card-title')?.textContent || card.querySelector('h3, h2')?.textContent || 'Project';
            const imgEl = card.querySelector('img');
            const imgSrc = imgEl ? (imgEl.dataset.src || imgEl.getAttribute('src')) : '/assets/images/placeholder-project.jpg';
            const excerpt = card.querySelector('.post-card-description')?.textContent || card.querySelector('.post-card-excerpt')?.textContent || '';
            const link = card.querySelector('a') ? card.querySelector('a').getAttribute('href') : '#';

            // populate detail panel
            const titleEl = detail.querySelector('.project-title');
            const yearEl = detail.querySelector('.project-year');
            const mediumEl = detail.querySelector('.project-medium');
            const descEl = detail.querySelector('.project-description');
            const imgWrap = detail.querySelector('.project-image img');
            const openLink = detail.querySelector('.project-open-link');

            if (titleEl) titleEl.textContent = title;
            if (descEl) descEl.textContent = excerpt;
            if (imgWrap) imgWrap.setAttribute('src', imgSrc);
            if (openLink) openLink.setAttribute('href', link);

            // optional: if the post's frontmatter includes date or medium, read data attributes
            if (yearEl) yearEl.textContent = card.dataset.year || '';
            if (mediumEl) mediumEl.textContent = card.dataset.medium || '';

            // bring detail into view on small screens
            if (window.innerWidth < 900) {
                detail.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

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
