// auth.js - Controls sliding panel states and authentication API calls

document.addEventListener('DOMContentLoaded', () => {
    let activeView = "login"; // Default state

    const cardBg = document.querySelector('.card-bg');
    const heroLogin = document.querySelector('.hero.login');
    const heroRegister = document.querySelector('.hero.register');
    const formLogin = document.querySelector('.form.login');
    const formRegister = document.querySelector('.form.register');

    function updateView() {
        if (activeView === "login") {
            cardBg.classList.add('login');
            heroLogin.classList.add('active');
            heroRegister.classList.remove('active');
            formLogin.classList.add('active');
            formRegister.classList.remove('active');
        } else {
            cardBg.classList.remove('login');
            heroLogin.classList.remove('active');
            heroRegister.classList.add('active');
            formLogin.classList.remove('active');
            formRegister.classList.add('active');
        }
    }

    // Toggle button handlers
    const toggleBtns = document.querySelectorAll('[data-toggle]');
    toggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            activeView = activeView === "login" ? "register" : "login";
            updateView();
        });
    });

    // Initialize view state
    updateView();

    // Login Form Submit
    const loginFormElement = document.querySelector('.form.login form');
    if (loginFormElement) {
        loginFormElement.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = loginFormElement.querySelector('input[type="email"]').value;
            const password = loginFormElement.querySelector('input[type="password"]').value;

            try {
                const res = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();
                if (data.success) {
                    showToast("Login successful! Redirecting to dashboard...", "success");
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 800);
                } else {
                    showToast(data.message || "Invalid credentials", "error");
                }
            } catch (err) {
                showToast("Server error during login", "error");
            }
        });
    }

    // Register Form Submit
    const registerFormElement = document.querySelector('.form.register form');
    if (registerFormElement) {
        registerFormElement.addEventListener('submit', async (e) => {
            e.preventDefault();
            const inputs = registerFormElement.querySelectorAll('input');
            const name = inputs[0].value;
            const email = inputs[1].value;
            const password = inputs[2].value;

            try {
                const res = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, password })
                });
                const data = await res.json();
                if (data.success) {
                    showToast("Registration successful! Redirecting to dashboard...", "success");
                    setTimeout(() => {
                        window.location.href = '/dashboard';
                    }, 800);
                } else {
                    showToast(data.message || "Registration failed", "error");
                }
            } catch (err) {
                showToast("Server error during registration", "error");
            }
        });
    }

    function showToast(msg, type) {
        const toast = document.getElementById('toast');
        if (!toast) return;
        toast.textContent = msg;
        toast.className = `toast ${type}`;
        toast.style.display = 'block';
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }
});
