const pasword = document.getElementById('password');
const toch = document.querySelector('login-btn')
const send = document.getElementById('send');
const errortext = document.getElementById('eror-text');
const p =document.createElement('p')
const loginCard = document.querySelector('.login-card');
p.appendChild(document.createTextNode(' حداقل کرکتر مجاز برای پسورد 7 کلمه است'))
p.id = 'eror-text'


send.addEventListener('click', function() {
    if (pasword.value.length < 7) {
        loginCard.appendChild(p);
    }
});