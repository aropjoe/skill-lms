// static/js/animations.js

console.log('Skill LMS Animations JavaScript loaded!');

document.addEventListener('DOMContentLoaded', () => {

    // Example: Animate elements on scroll (requires more setup, this is conceptual)
    const animateOnScrollElements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible'); // Add a class to trigger CSS animation
                observer.unobserve(entry.target); // Stop observing once visible
            }
        });
    }, { threshold: 0.1 }); // Trigger when 10% of the element is visible

    animateOnScrollElements.forEach(element => {
        observer.observe(element);
    });

    // Example: Simple hover animation using JS (less common than CSS, but adds JS)
    const hoverElements = document.querySelectorAll('.js-hover-animate');
    hoverElements.forEach(element => {
        element.addEventListener('mouseover', () => {
            element.style.transform = 'scale(1.05)';
            element.style.transition = 'transform 0.3s ease';
        });
        element.addEventListener('mouseout', () => {
            element.style.transform = 'scale(1)';
        });
    });

});

// Example: Function to trigger a modal animation
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden'); // Assuming 'hidden' utility class
        modal.classList.add('fade-in'); // Assuming 'fade-in' animation class
        console.log(`Opening modal: ${modalId}`);
    }
}

function closeModal(modalId) {
     const modal = document.getElementById(modalId);
     if (modal) {
         modal.classList.remove('fade-in');
         modal.classList.add('fade-out'); // Assuming a 'fade-out' animation class
         modal.addEventListener('animationend', () => {
             modal.classList.add('hidden');
             modal.classList.remove('fade-out');
         }, { once: true }); // Remove listener after one trigger
         console.log(`Closing modal: ${modalId}`);
     }
}