const uploadBtn = document.getElementById("upload-btn");
const uploadInput = document.getElementById("profile-upload");
const previewImage = document.getElementById("profile-preview-image");

uploadBtn.addEventListener("click", () => {
    uploadInput.click();
});

uploadInput.addEventListener("change", (event) => {

    const file = event.target.files[0];

    if(!file){
        return;
    }

    const imageUrl = URL.createObjectURL(file);

    previewImage.src = imageUrl;

});