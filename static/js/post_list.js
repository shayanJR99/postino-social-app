const postsContainer =
    document.getElementById('posts-container');
const params =
    new URLSearchParams(window.location.search);
const post = params.get('post');
if (post) {
    const card = document.createElement('div');
    card.classList.add('post-card');
    card.innerHTML = `
        <div class="user-info">
            <img
                class="profile-img"
                src="../../media/ghost.png"
                alt="profile">
                
            <p>@prmfi</p>
        </div>

        <p class="post-text">
            ${post}
        </p>
    `;

    postsContainer.appendChild(card);
}
const logoutBtn = document.getElementById("logoutBtn");

const logoutModal = document.getElementById("logoutModal");

const cancelBtn = document.getElementById("cancelBtn");

logoutBtn.addEventListener("click", function(){

    logoutModal.classList.add("active");

});

cancelBtn.addEventListener("click", function(){

    logoutModal.classList.remove("active");

});

logoutModal.addEventListener("click", function(event){

    if(event.target === logoutModal){

        logoutModal.classList.remove("active");

    }

});

document.addEventListener("keydown", function(event){

    if(event.key === "Escape"){

        logoutModal.classList.remove("active");

    }

});
