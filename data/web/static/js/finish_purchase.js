const finishButton = document.getElementById("finishPurchase");
const actUser = document.getElementById("data").getAttribute("data-user");
const cartUser = document.getElementById("data").getAttribute("data-con");

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