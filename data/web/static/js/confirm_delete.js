const btnDelete = document.getElementById('btnDelete');
const modalDelete = document.querySelector('.modalDelete');
const btnCancel = document.getElementById('btnCancel');
const btnConfirm = document.getElementById('btnConfirm');
const span = document.getElementsByClassName("close")[0];
const deleteUrl = btnConfirm.dataset.deleteUrl;

btnDelete.onclick = function() {
    modalDelete.style.display = "block";
}

span.onclick = function() {
    modalDelete.style.display = "none";
}

c

btnConfirm.onclick = function() {
    window.location.href = deleteUrl;
}