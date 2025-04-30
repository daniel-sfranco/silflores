const ticketButton = document.getElementById("generateTicket")
const username = ticketButton.getAttribute('data-user')
const nameuser = ticketButton.getAttribute('data-name')

ticketButton.onclick = function(){
    fetch(`/cart/${username}/getTicket`, {
        method: "POST",
        headers: {
            'X-Requested-With': "XMLHttpRequest",
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data.url){
            const ticketUrl = data.url
            const ticketWindow = window.open(ticketUrl, '_blank')
            ticketWindow.focus()
        }
    })
}