const imageInput = document.getElementById('id_photo');
const previewImage = document.querySelector('.user_photo');
const clearImage = document.getElementById('photo-clear_id')

previewImage.addEventListener('click', function() {
    imageInput.click();
})

imageInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
        previewImage.src = e.target.result;
    }

    reader.readAsDataURL(file);
});

 function handleCheckboxChange(checkbox) {
    if(checkbox.checked){
        previewImage.src = '/media/fallback_user.png';
    } else {
        previewImage.src = '{{ widget.value.url }}';
    }
}
