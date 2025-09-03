const quantityInputs = document.getElementsByClassName("quantityInput")

for(let i = 0; i < quantityInputs.length; i++){
    quantityInputs[i].addEventListener('change', function(event) {
        if(event.target.value){
            const pk = event.target.id;
            const quantity = event.target.value;
            fetch('/cart/setQuantity', {
                method:'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    'pk': pk,
                    'quantity': quantity
                })
            })
            .then(response => {
                if(response.ok){
                    window.location.href = window.location.href;
                }
            })
            .catch(error => console.error('Erro ao definir quantidade:', error));
        }
    })
}