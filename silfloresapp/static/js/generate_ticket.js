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
    .then(response => response.blob())
    .then(Blob => {
        const url = window.URL.createObjectURL(Blob)
        const a = document.createElement("a")
        a.href = url
        a.download = `Etiqueta ${nameuser}.pdf`
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)

    })
}