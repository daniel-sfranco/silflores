const ticketButton = document.getElementById("generateTicket")
const username = ticketButton.getAttribute('data-user')

ticketButton.onclick = function(){
    fetch(`/cart/${username}/getTicket`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        window.open(data.url, '_blank')
    })
}