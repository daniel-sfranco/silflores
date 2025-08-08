const photoCards = document.querySelectorAll('.card');
const photoConfirm = document.getElementById("photoConfirm");
const photoCancel = document.getElementById("photoCancel");
const modalDelete = document.getElementById("photoModalDelete");
let deleteUrl = ""

document.getElementById("photo-carousel").addEventListener("click", function (event) {
    const clickedElement = event.target;
    if (clickedElement.tagName === "IMG" && clickedElement.hasAttribute("data-delete-url")) {
        deleteUrl = clickedElement.getAttribute("data-delete-url");
        modalDelete.style.display = "block";
    }
});

photoConfirm.onclick = function () {
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
    });
}

photoCancel.onclick = function () {
    modalDelete.style.display = "none";
}
