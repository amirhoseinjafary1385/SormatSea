// Initialize Glide.js
document.addEventListener('DOMContentLoaded', function() {
    // Default Glide config
    const glideConfig = {
        type: 'carousel',
        startAt: 0,
        perView: 3,
        gap: 24,
        autoplay: 5000,
        hoverpause: true,
        animationDuration: 600,
        breakpoints: {
            1200: { perView: 3 },
            991: { perView: 2 },
            600: { perView: 1 }
        }
    };

    function addNavigationControls(glide) {
        const nextBtn = document.querySelector('.glide__arrow--next');
        const prevBtn = document.querySelector('.glide__arrow--prev');
        if (nextBtn) nextBtn.addEventListener('click', () => glide.go('>'));
        if (prevBtn) prevBtn.addEventListener('click', () => glide.go('<'));
    }

    // Expose addSlide globally with error handling
    window.addGlideSlide = function(content) {
        const glideTrack = document.querySelector('.glide__track .glide__slides');
        if (glideTrack) {
            const slide = document.createElement('li');
            slide.className = 'glide__slide';
            slide.innerHTML = content;
            glideTrack.appendChild(slide);
            if (window.glideInstance) window.glideInstance.update();
        } else {
            console.warn('Glide track not found.');
        }
    };

    // Expose removeLastSlide globally with error handling
    window.removeLastGlideSlide = function() {
        const glideTrack = document.querySelector('.glide__track .glide__slides');
        if (glideTrack && glideTrack.lastElementChild) {
            glideTrack.removeChild(glideTrack.lastElementChild);
            if (window.glideInstance) window.glideInstance.update();
        } else {
            console.warn('No slide to remove.');
        }
    };


    if (typeof Glide === 'undefined') {
        console.warn('Glide.js library is not loaded.');
        return;
    }
    const glideEl = document.querySelector('.glide');
    if (!glideEl) {
        console.warn('Glide.js carousel element not found.');
        return;
    }
    const slides = glideEl.querySelectorAll('.glide__slide');
    if (slides.length === 0) {
        console.warn('No slides found in .glide element.');
        return;
    }
    try {
        const glide = new Glide('.glide', glideConfig);
        window.glideInstance = glide;
        glide.on('run.after', () => {
            const curr = glide.index;
            document.dispatchEvent(new CustomEvent('glide:slideChanged', { detail: { index: curr } }));
        });
        glide.mount();
        addNavigationControls(glide);
        // Example: window.addGlideSlide('<div>New Slide</div>');
        // Example: window.removeLastGlideSlide();
    } catch (err) {
        console.warn('Glide init error:', err);
    }
});