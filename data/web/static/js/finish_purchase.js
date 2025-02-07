const finishButton = document.getElementById("finishPurchase");
const cartUser = document.getElementById("data").getAttribute("data-user");

finishButton.onclick = function() {
    fetch(`/cart/${cartUser}/processPayment`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
}