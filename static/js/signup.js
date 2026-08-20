const signupForm = document.getElementById('signupForm');
const signupMessage = document.getElementById('signupMessage');

function showSignupMessage(message, type) {
    signupMessage.textContent = message;
    signupMessage.className = `form-message form-message--${type}`;
}

signupForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const diabetesType = document.getElementById('diabetesType').value;

    // ==============================
    // CLIENT-SIDE VALIDATION
    // ==============================

    if (!username || !fullName || !email || !password || !confirmPassword || !diabetesType) {
        showSignupMessage(
            'Please complete all fields.',
            'error'
        )
        return;
    }

    if (password !== confirmPassword) {
        showSignupMessage(
            'Password do not match.',
            'error'
        )
        return;
    }

    // ==============================
    // REGISTER API
    // ==============================

    try {
        const response = await fetch('/api/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                full_name: fullName,
                diabetes_type: diabetesType
            })
        });

        const result = await response.json();

        console.log('Register status:', response.status);
        console.log('Register response:', result);

        if (!response.ok) {
            showSignupMessage(
                result.error || 'Failed to create account.',
                'error'
            );
            return;
        }

        showSignupMessage(
            'Account created successfully. Redirecting to login...',
            'success'
        );

        // Redirect to login
        window.location.href = '/auth/login/';

    } catch (error) {
        console.error('Register error:', error);

        showSignupMessage(
            'Something went wrong. Please try again.',
            'error'
        );
    }
});