const imageInput = document.getElementById("imageInput");
const previewContainer = document.getElementById("previewContainer");

imageInput.addEventListener("change", () => {

    previewContainer.innerHTML = "";

    const files = [...imageInput.files];

    if(files.length > 3){

        alert("حداکثر 3 عکس مجاز است");

        imageInput.value = "";

        return;
    }

    files.forEach(file => {

        const reader = new FileReader();

        reader.onload = function(e){

            const img = document.createElement("img");

            img.src = e.target.result;

            previewContainer.appendChild(img);
        };

        reader.readAsDataURL(file);

    });

});