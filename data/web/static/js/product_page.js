const authInput = document.getElementById("auth")
const addButton = document.getElementById("btnAddCart");
const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
const quantity = document.getElementById("quantityInput")
const slug = addButton.getAttribute("data-slug")
addButton.onclick = function(){
    if(quantity.value != ''){
        fetch('/cart/add', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'slug': slug,
                'quantity': quantity.value,
            })
        })
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                const next = new URL(window.location.href); // Pega a URL atual
                window.location.href = '/user/login?next=', next
                } else {
                console.error("Erro ao adicionar ao carrinho:", response.status, response.statusText);
                }
            } else {
                window.location.href = '/cart/' + authInput.getAttribute("data-user") + '/page'; // Redirect to the cart page
            }
        })
        .catch(error => {
            console.error("Erro na solicitação:", error);
        });
    }
}