const trackButton = document.getElementById("trackShipment");

if (trackButton) {
    const username = trackButton.getAttribute('data-user');
    trackButton.addEventListener('click', function() {
        fetch(`/cart/${username}/track`, {
            method: "GET"
        })
        .then((response) => response.json())
        .then((data) => {
            if(data.trackingUrl){
                const url = data.trackingUrl;
                const trackingWindow = window.open(url, '_blank');
                trackingWindow.focus();
            }
        })
        .catch(error => console.error('Erro ao rastrear envio:', error));
    });
}
