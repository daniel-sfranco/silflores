const modalSize = document.querySelector(".modalSize");
const spanClose = document.getElementById("closeSize");
const btnSetSize = document.getElementById("btnSize");
const sizeSelect = document.getElementById("size"); // Use "sizeSelect" for the select element
const sizeCancel = document.getElementById("sizeCancel");
const sizeConfirm = document.getElementById('sizeConfirm');
const data = document.getElementById("data")
let selectQty = document.getElementById("quantity")
let selectedSize = parseFloat(data.dataset.size); // Store the selected size
const productSlug = data.dataset.slug;
let authenticated = data.dataset.auth;


sizeConfirm.onclick = click;

btnSetSize.onclick = function () {
    if(authenticated == 'True'){
        modalSize.style.display = "block";
        selectedSize = parseFloat(sizeSelect.value);
    } else {
        window.location.href = '/user/login?next=' + encodeURIComponent(window.location.href);
    }
};

spanClose.onclick = function() {
    modalSize.style.display = "none";
};

sizeCancel.onclick = function() {
    modalSize.style.display = "none";
};

sizeSelect.addEventListener('change', function() {
    selectedSize = parseFloat(sizeSelect.value);
});


function click () {
    const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    fetch('/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'slug': productSlug,
            'size': selectedSize,
            'quantity': parseInt(selectQty.value)
        })
    })
    .then(response => {
        if (response.status == 200) {
            modalSize.style.display = "none";
            window.location.href = '/cart'; // Redirect to the cart page
        } else {
            alert("Erro ao adicionar ao carrinho. Tente novamente.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
