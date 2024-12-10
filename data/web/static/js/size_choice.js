const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;
const modalSize = document.querySelector(".modalSize");
const spanClose = document.getElementById("closeSize");
const btnSizeElements = document.getElementsByClassName("btnSize");
const btnAddCart = document.getElementById("btnAddCart");
let sizeSelect = document.getElementById("size");
const sizeCancel = document.getElementById("sizeCancel");
const sizeConfirm = document.getElementById('sizeConfirm');
const data = document.getElementById("data")
const selectQty = document.getElementById("quantity")
const sizeOptions = document.querySelectorAll(".option");
const sizeDiv = document.getElementById("chooseSize");
const textQuantity = document.getElementById("pQuantity");
let authenticated = document.getElementById("data").getAttribute("data-auth")
let productSlug = '';


sizeConfirm.onclick = function() {
    if(sizeSelect.value != '' && productSlug != ''){
        click()
    }
};

btnAddCart.onclick = function () {
    if(authenticated == 'True'){
        modalSize.style.display = "block";
        productSlug = btnAddCart.getAttribute('data-slug');
    } else {
        window.location.href = '/user/login?next=' + encodeURIComponent(window.location.href);
    }
};

Array.from(btnSizeElements).forEach(btn => {
    btn.onclick = function() {
        productSlug = btn.getAttribute('data-slug');
        fetch('/cart/' + productSlug + '/getsize', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        })
        .then(data => data.text())
        .then(data => {
            let array = data.split(' ')
            console.log(array)
            if(array[0] != ''){
                let newHtml =`<p>Escolha um tamanho para o produto</p>
                <select name="size" id="size">`
                for(let i = 0; i < array.length; i++){
                    newHtml += '<option value=' + array[i] + ' class="option">' + array[i] + '</option>'
                }
                newHtml += "</select>"
                sizeDiv.innerHTML = newHtml;
            } else {
                sizeDiv.innerHTML =
                `<p>Escolha um tamanho para o produto</p>
                <input type="text" id="size">`;
            }
            sizeSelect = document.getElementById("size");
        })
        modalSize.style.display = "block";
    }
})

spanClose.onclick = function() {
    modalSize.style.display = "none";
};

sizeCancel.onclick = function() {
    modalSize.style.display = "none";
};


function click () {
    fetch('/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'slug': productSlug,
            'size': sizeSelect.value,
            'quantity': parseInt(selectQty.value)
        })
    })
    .then(response => {
        if (!response.ok) {
          if (response.status === 401) {
            const next = new URL(window.location.href); // Pega a URL atual
            console.log(respose.statusText)
          } else {
            console.error("Erro ao adicionar ao carrinho:", response.status, response.statusText);
          }
        } else {
            console.log('all right!');
            window.location.href = '/cart'; // Redirect to the cart page
        }
      })
      .catch(error => {
        console.error("Erro na solicitação:", error);
      });
}
