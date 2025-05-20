// static/js/tabs.js

console.log('Skill LMS Tabs JavaScript loaded!');

document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');

    // Function to activate a specific tab
    const activateTab = (button) => {
         const lessonId = button.dataset.lessonId;

        // Deactivate all buttons
        tabButtons.forEach(btn => {
            btn.setAttribute('aria-selected', 'false');
            btn.setAttribute('tabindex', '-1');
            btn.classList.remove('bg-indigo-600', 'text-white'); // Use indigo-600 for active state
            btn.classList.add('text-gray-700', 'hover:bg-gray-100');
        });

        // Hide all tab contents
        tabContents.forEach(content => {
            content.classList.add('hidden');
            content.classList.remove('block');
        });

        // Activate the clicked button
        button.setAttribute('aria-selected', 'true');
        button.setAttribute('tabindex', '0');
        button.classList.remove('text-gray-700', 'hover:bg-gray-100');
        button.classList.add('bg-indigo-600', 'text-white'); // Use indigo-600 for active state

        // Show the corresponding tab content
        const targetContent = document.getElementById(`panel-${lessonId}`);
        if (targetContent) {
            targetContent.classList.remove('hidden');
            targetContent.classList.add('block');
        }
    };


    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            activateTab(button);
        });
    });

    // Activate the first tab on load if no specific tab is indicated (e.g., via URL hash)
    const firstActiveButton = document.querySelector('.tab-button[aria-selected="true"]');
    if (!firstActiveButton) {
        const firstButton = document.querySelector('.tab-button');
        if (firstButton) {
            activateTab(firstButton); // Simulate click on the first button
        }
    } else {
         // If a tab is marked active by Django (e.g., the first one), ensure its content is shown
         const initialLessonId = firstActiveButton.dataset.lessonId;
         const initialContent = document.getElementById(`panel-${initialLessonId}`);
         if (initialContent) {
             initialContent.classList.remove('hidden');
             initialContent.classList.add('block');
         }
    }

     // Optional: Handle deep linking to a specific lesson tab via URL hash (e.g., #lesson-5)
    if (window.location.hash) {
        const targetLessonSlug = window.location.hash.substring(1); // Remove the '#'
        // Find the button corresponding to the lesson slug (you might need to add slug as data attribute)
        // Or, if using lesson ID in hash (e.g., #panel-123), find the panel and then its button
        const targetPanel = document.getElementById(targetLessonSlug); // Assuming hash matches panel ID
        if (targetPanel) {
             const targetButtonId = targetPanel.getAttribute('aria-labelledby');
             const targetButton = document.getElementById(targetButtonId);
             if (targetButton) {
                 activateTab(targetButton);
                 // Optional: Scroll to the top of the content area after switching tab
                  targetPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
             }
        }
    }
});