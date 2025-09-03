const btnDelete = document.getElementById('btnDelete');
const modalDelete = document.querySelector('.modalDelete');
const btnCancel = document.getElementById('deleteCancel');
const btnConfirm = document.getElementById('deleteConfirm');
const span = document.getElementsByClassName("close")[0];
const deleteUrl = btnConfirm.dataset.deleteUrl;

if (btnDelete) {
    btnDelete.addEventListener('click', function() {
        modalDelete.style.display = "block";
    });
}

if (span) {
    span.addEventListener('click', function() {
        modalDelete.style.display = "none";
    });
}

if (btnCancel) {
    btnCancel.addEventListener('click', function() {
        modalDelete.style.display = "none";
    });
}

if (btnConfirm) {
    btnConfirm.addEventListener('click', function() {
        window.location.href = deleteUrl;
    });
}