const form = document.getElementById('login-form');
const email = document.getElementById('email');
const password = document.getElementById('password');
const loginCard = document.querySelector('.login-card');

function showError(message) {
    let errorElement = document.getElementById('error-text');

    if (!errorElement) {
        errorElement = document.createElement('p');
        errorElement.id = 'error-text';
        errorElement.classList.add('error-text');
        loginCard.appendChild(errorElement);
    }

    errorElement.textContent = message;
}

function removeError() {
    const errorElement = document.getElementById('error-text');
    if (errorElement) errorElement.remove();
}

form.addEventListener('submit', (e) => {
    e.preventDefault(); // جلوی ارسال اولیه

    removeError();

    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();

    // validation
    if (!emailValue) return showError('ایمیل را وارد کنید');
    if (!emailValue.includes('@')) return showError('ایمیل معتبر نیست');
    if (!passwordValue) return showError('رمز عبور را وارد کنید');
    if (passwordValue.length < 7) return showError('حداقل 7 کاراکتر لازم است');

    console.log('فرم معتبر است، ارسال به Django...');

    form.submit(); // ارسال واقعی به بک‌اند
});