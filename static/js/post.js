const sendBtn = document.querySelector('.send-btn');
const textarea = document.querySelector('.thread-input');

sendBtn.addEventListener('click', () => {

    const text = textarea.value.trim();

    if (!text) {
        alert('متن پست را وارد کنید');
        return;
    }

    window.location.href =
        `index.html?post=${encodeURIComponent(text)}`;

});