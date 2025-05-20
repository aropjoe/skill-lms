// static/js/main.js

console.log('Skill LMS Main JavaScript loaded!');

document.addEventListener('DOMContentLoaded', () => {
    // Example: Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop,
                    behavior: 'smooth' // Smooth scroll animation
                });
            }
        });
    });

    // Example: Simple click handler for a hypothetical button
    const myButton = document.getElementById('myAwesomeButton');
    if (myButton) {
        myButton.addEventListener('click', () => {
            alert('Button clicked!'); // Replace with a more sophisticated action
            console.log('Awesome button was clicked.');
        });
    }

    // Example: Add a class to the body when the page is fully loaded
    window.addEventListener('load', () => {
        document.body.classList.add('page-loaded');
        console.log('Page fully loaded.');
    });

    // Example: Basic responsive check (can be done with CSS, but JS adds complexity)
    const checkScreenWidth = () => {
        if (window.innerWidth < 768) {
            document.body.classList.add('is-mobile');
            document.body.classList.remove('is-desktop');
        } else {
            document.body.classList.add('is-desktop');
            document.body.classList.remove('is-mobile');
        }
    };

    checkScreenWidth(); // Initial check
    window.addEventListener('resize', checkScreenWidth); // Check on resize

});

// Example function that might be called from other scripts or templates
function showWelcomeMessage(username) {
    console.log(`Hello, ${username}! Welcome to Skill LMS.`);
    // You could use this to display a dynamic welcome banner or modal
}