const form = document.getElementById('signup-form');

const email = document.getElementById('email');
const password1 = document.getElementById('password1');
const password2 = document.getElementById('password2');

const loginCard = document.querySelector('.login-card');

function showError(message){

    let errorElement = document.getElementById('error-text');

    if(!errorElement){

        errorElement = document.createElement('p');
        errorElement.id = 'error-text';

        loginCard.appendChild(errorElement);
    }

    errorElement.textContent = message;
}

function removeError(){

    const errorElement = document.getElementById('error-text');

    if(errorElement){
        errorElement.remove();
    }
}

form.addEventListener('submit', function(e){

    e.preventDefault();

    removeError();

    const emailValue = email.value.trim();
    const password1Value = password1.value.trim();
    const password2Value = password2.value.trim();

    if(!emailValue){
        showError('ایمیل را وارد کنید');
        return;
    }

    if(!emailValue.includes('@')){
        showError('ایمیل معتبر نیست');
        return;
    }

    if(!password1Value){
        showError('رمز عبور را وارد کنید');
        return;
    }

    if(password1Value.length < 7){
        showError('حداقل 7 کاراکتر برای رمز عبور لازم است');
        return;
    }

    if(password1Value !== password2Value){
        showError('پسوردها یکی نیستند');
        return;
    }

    alert('ثبت نام با موفقیت انجام شد');
});