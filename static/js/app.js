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