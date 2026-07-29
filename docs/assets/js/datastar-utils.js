// Datastar Utilities for Explosive Website Template
// Helper functions and utilities for working with Datastar

/**
 * Initialize Datastar-powered components
 */
function initDatastarComponents() {
    console.log('Datastar components initialized');

    // Datastar auto-initializes from CDN, no manual initialization needed

    initCarouselKeyboardNavigation();
    initCarouselTouchSupport();
}

/**
 * Add keyboard navigation to carousels
 */
function initCarouselKeyboardNavigation() {
    const carousels = document.querySelectorAll('.carousel');

    carousels.forEach(carousel => {
        carousel.setAttribute('tabindex', '0');

        carousel.addEventListener('keydown', (e) => {
            const prevButton = carousel.querySelector('.carousel-control-prev');
            const nextButton = carousel.querySelector('.carousel-control-next');

            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    if (prevButton) prevButton.click();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    if (nextButton) nextButton.click();
                    break;
                case 'Home':
                    e.preventDefault();
                    const firstIndicator = carousel.querySelector('.carousel-indicator:first-child');
                    if (firstIndicator) firstIndicator.click();
                    break;
                case 'End':
                    e.preventDefault();
                    const lastIndicator = carousel.querySelector('.carousel-indicator:last-child');
                    if (lastIndicator) lastIndicator.click();
                    break;
            }
        });
    });
}

/**
 * Add touch/swipe support to carousels
 */
function initCarouselTouchSupport() {
    const carousels = document.querySelectorAll('.carousel');

    carousels.forEach(carousel => {
        let touchStartX = 0;
        let touchEndX = 0;
        const minSwipeDistance = 50;

        carousel.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });

        carousel.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe(carousel, touchStartX, touchEndX, minSwipeDistance);
        }, { passive: true });
    });
}

/**
 * Handle swipe gesture
 */
function handleSwipe(carousel, startX, endX, minDistance) {
    const diff = startX - endX;

    if (Math.abs(diff) > minDistance) {
        if (diff > 0) {
            // Swipe left - next slide
            const nextButton = carousel.querySelector('.carousel-control-next');
            if (nextButton) nextButton.click();
        } else {
            // Swipe right - previous slide
            const prevButton = carousel.querySelector('.carousel-control-prev');
            if (prevButton) prevButton.click();
        }
    }
}

/**
 * Helper function to create Datastar signal
 * @param {string} name - Signal name
 * @param {*} initialValue - Initial value
 * @returns {string} - Datastar attribute string
 */
function createSignal(name, initialValue) {
    return `data-signal-${name}="${JSON.stringify(initialValue).replace(/"/g, '&quot;')}"`;
}

/**
 * Helper function to create Datastar computed value
 * @param {string} name - Computed name
 * @param {string} expression - JavaScript expression
 * @returns {string} - Datastar attribute string
 */
function createComputed(name, expression) {
    return `data-computed-${name}="${expression.replace(/"/g, '&quot;')}"`;
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDatastarComponents);
} else {
    initDatastarComponents();
}

