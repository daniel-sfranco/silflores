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
    .then(response => {
        if(response.headers.get('content-type').includes('application/json') && response.status === 200){
            response.json().then(json => {
                if (json.url) {
                    window.open(json.url, '_blank');
                }
            })
        } else {
            response.blob().then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = `Etiqueta ${nameuser}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            });
        }
    })
}