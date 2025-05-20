// static/js/forms.js

console.log('Skill LMS Forms JavaScript loaded!');

document.addEventListener('DOMContentLoaded', () => {

    // Example: Basic client-side validation for a signup form
    const signupForm = document.getElementById('signupForm'); // Assuming your signup form has this ID

    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            let isValid = true;

            // Get form elements
            const usernameInput = this.querySelector('input[name="username"]');
            const passwordInput = this.querySelector('input[name="password"]');
            const emailInput = this.querySelector('input[name="email"]');

            // Basic validation checks (can be much more complex)
            if (usernameInput && usernameInput.value.trim() === '') {
                alert('Username cannot be empty.'); // Replace with better UI feedback
                isValid = false;
            }

            if (passwordInput && passwordInput.value.trim() === '') {
                 alert('Password cannot be empty.'); // Replace with better UI feedback
                 isValid = false;
            } else if (passwordInput && passwordInput.value.length < 8) {
                 alert('Password must be at least 8 characters.'); // Replace with better UI feedback
                 isValid = false;
            }

            if (emailInput && emailInput.value.trim() !== '' && !validateEmail(emailInput.value)) {
                alert('Please enter a valid email address.'); // Replace with better UI feedback
                isValid = false;
            }


            if (!isValid) {
                event.preventDefault(); // Prevent form submission if validation fails
                console.log('Form validation failed.');
            } else {
                 console.log('Form validation successful.');
                 // Allow form submission
            }
        });
    }

    // Helper function for email validation (basic regex)
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }

    // Example: Real-time password strength indicator (conceptual)
    const passwordInput = document.getElementById('password'); // Assuming password input has this ID
    const passwordStrengthIndicator = document.getElementById('passwordStrength'); // Hypothetical element

    if (passwordInput && passwordStrengthIndicator) {
        passwordInput.addEventListener('input', () => {
            const password = passwordInput.value;
            let strength = 0;

            if (password.length > 5) strength++;
            if (password.length > 10) strength++;
            if (/[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^A-Za-z0-9]/.test(password)) strength++;

            // Update indicator based on strength (requires corresponding HTML/CSS)
            passwordStrengthIndicator.textContent = `Strength: ${strength}/5`;
            // Add classes to the indicator for visual feedback (e.g., weak, medium, strong)
        });
    }

});