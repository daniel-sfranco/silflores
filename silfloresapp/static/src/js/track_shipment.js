const trackButton = document.getElementById("trackShipment")
const username = trackButton.getAttribute('data-user')

trackButton.onclick = function() {
    fetch(`/cart/${username}/track`, {
        method: "GET"
    })
    .then((response) => response.json())
    .then((data) => {
        if(data.trackingUrl){
            const url = data.trackingUrl
            const trackingWindow = window.open(url, '_blank')
            trackingWindow.focus()
        }
    })
}
