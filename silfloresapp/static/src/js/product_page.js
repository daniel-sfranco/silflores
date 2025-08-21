const authInput = document.getElementById("auth")
const addButton = document.getElementById("btnAddCart");
const slug = addButton.getAttribute("data-slug")

addButton.onclick = function(){
    fetch('/cart/add', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'slug': slug,
        })
    })
    .then(response => {
        if (response.ok) {
            if(authInput.getAttribute("data-user")){
                window.location.href = '/cart/' + authInput.getAttribute("data-user") + '/page';
            } else {
                actUrl = new URL(window.location.href)
                window.location.href = `/user/login/?next=${actUrl.pathname}`;
            }
        } else {
            console.error("Erro ao adicionar ao carrinho:", response.status, response.statusText);
        }
    })
    .catch(error => {
        console.error("Erro na solicitação:", error);
    });
}
