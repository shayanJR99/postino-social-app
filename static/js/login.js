const email = document.getElementById('email');
const password = document.getElementById('password');
const send = document.getElementById('send');
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

    if (errorElement) {
        errorElement.remove();
    }
}

send.addEventListener('click', () => {

    removeError();

    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();

    if (!emailValue) {
        showError('ایمیل را وارد کنید');
        return;
    }

    if (!emailValue.includes('@')) {
        showError('ایمیل معتبر نیست');
        return;
    }

    if (!passwordValue) {
        showError('رمز عبور را وارد کنید');
        return;
    }

    if (passwordValue.length < 7) {
        showError('حداقل 7 کاراکتر برای رمز عبور لازم است');
        return;
    }

    console.log('فرم معتبر است');

});