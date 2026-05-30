const pasword = document.getElementById('password1');
const send = document.getElementById('send');
const loginCard = document.querySelector('.login-card');

const p = document.createElement('p');
p.textContent = ' حداقل کرکتر مجاز برای پسورد 7 کلمه است';
p.id = 'eror-text';

send.addEventListener('click', function(event) {

    event.preventDefault();

    if (pasword.value.length < 7) {

        if (!document.getElementById('eror-text')) {
            loginCard.appendChild(p);
        }

    }

});