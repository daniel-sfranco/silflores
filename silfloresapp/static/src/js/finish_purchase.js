const finishButton = document.getElementById("finishPurchase");
const user = document.getElementById("data").getAttribute("data-user");

finishButton.onclick = function() {
    const freightOption = document.querySelector('input[name="freight_options"]:checked')
    const freightValue = document.getElementById(freightOption.value)
    fetch(`/cart/${user}/processPayment`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'freight_option': parseInt(freightOption.getAttribute('data-id')),
            'freight_value': freightValue.innerText
        })
    })
    .then(response => response.json())
    .then(data => {
        window.location.href=data.payment_link
    })
}
