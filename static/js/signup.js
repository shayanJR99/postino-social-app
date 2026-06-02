form.addEventListener('submit', function (e) {

    removeError();

    const emailValue = email.value.trim();
    const password1Value = password1.value.trim();
    const password2Value = password2.value.trim();

    if (!emailValue) {
        e.preventDefault();
        return showError('ایمیل را وارد کنید');
    }

    if (!emailValue.includes('@')) {
        e.preventDefault();
        return showError('ایمیل معتبر نیست');
    }

    if (!password1Value) {
        e.preventDefault();
        return showError('رمز عبور را وارد کنید');
    }

    if (password1Value.length < 7) {
        e.preventDefault();
        return showError('حداقل 7 کاراکتر لازم است');
    }

    if (password1Value !== password2Value) {
        e.preventDefault();
        return showError('پسوردها یکی نیستند');
    }

    console.log('ارسال به Django');
});