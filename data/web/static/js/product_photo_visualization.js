const photos = document.getElementsByClassName('product_photo');
const photoModalDelete = document.querySelector('.modal');
const btnCancel = document.getElementById('btnCancel');
const btnConfirm = document.getElementById('btnConfirm');
const span = document.querySelector('.close');
const deleteUrl = btnConfirm.dataset.deleteUrl;
const actUrl = window.location.href;
let deleted;

photoModalDelete.style.display = 'none';

for(let i = 0; i < photos.length; i++){
    photos[i].addEventListener('click', function() {
        deleted = this;
        photoModalDelete.style.display = 'block';
        console.log(deleted.dataset.deleteUrl);
    })
}

span.onclick = function() {
    photoModalDelete.style.display = "none";
}

btnCancel.onclick = function() {
    window.event.preventDefault();
    photoModalDelete.style.display = "none";
}

btnConfirm.addEventListener('click', function() {
    window.event.preventDefault();
    photoModalDelete.style.display = "none";
    const deleteUrl = deleted.dataset.deleteUrl;
    window.location.href = deleteUrl;
})