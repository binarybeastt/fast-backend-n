document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:8000';

    // Handle registration form submission
    document.getElementById('register-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('register-username').value;
        const password = document.getElementById('register-password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                document.getElementById('output').innerText = 'Registration successful!';
            } else {
                const errorData = await response.json();
                document.getElementById('output').innerText = `Registration failed: ${errorData.detail}`;
            }
        } catch (error) {
            document.getElementById('output').innerText = `Error: ${error.message}`;
        }
    });

    // Handle login form submission
    document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        try {
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept': 'application/json'
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.access_token);
                document.getElementById('output').innerText = 'Login successful!';
            } else {
                const errorData = await response.json();
                document.getElementById('output').innerText = `Login failed: ${errorData.detail}`;
            }
        } catch (error) {
            document.getElementById('output').innerText = `Error: ${error.message}`;
        }
    });

    // Handle protected route access
    document.getElementById('access-protected').addEventListener('click', async () => {
        const token = localStorage.getItem('token');

        if (!token) {
            document.getElementById('output').innerText = 'Please log in first.';
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/protected-route/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                document.getElementById('output').innerText = `Protected data: ${JSON.stringify(data)}`;
            } else {
                const errorData = await response.json();
                document.getElementById('output').innerText = `Access denied: ${errorData.detail}`;
            }
        } catch (error) {
            document.getElementById('output').innerText = `Error: ${error.message}`;
        }
    });
});
