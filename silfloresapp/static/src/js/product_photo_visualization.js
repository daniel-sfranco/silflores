const photoCards = document.querySelectorAll('.card');
const photoConfirm = document.getElementById("photoConfirm");
const photoCancel = document.getElementById("photoCancel");
const modalDelete = document.getElementById("photoModalDelete");
let deleteUrl = "";

if (document.getElementById("photo-carousel")) {
    document.getElementById("photo-carousel").addEventListener("click", function (event) {
        const clickedElement = event.target;
        if (clickedElement.tagName === "IMG" && clickedElement.hasAttribute("data-delete-url")) {
            deleteUrl = clickedElement.getAttribute("data-delete-url");
            modalDelete.style.display = "block";
        }
    });
}

if (photoConfirm) {
    photoConfirm.addEventListener('click', function (event) {
        event.preventDefault();
        fetch(deleteUrl, {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                modalDelete.style.display = "none";
            } else {
                console.error("Error deleting photo:", data.error);
            }
            window.location.href = window.location.href;
        })
        .catch(error => console.error('Erro ao deletar foto:', error));
    });
}

if (photoCancel) {
    photoCancel.addEventListener('click', function () {
        modalDelete.style.display = "none";
    });
}
