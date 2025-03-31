const filterButton = document.querySelector(".dropButton")
const dropdownContent = document.querySelector(".dropdownContent")
const allCheckbox = document.getElementById('tag-all');
const lowerPrice = document.getElementById('lowerPrice');
const upperPrice = document.getElementById('upperPrice');
const stockAvaliable = document.getElementById("stockAvaliable");
const productCards = Array.from(document.getElementsByClassName("card"));
let tagCheckboxes = document.getElementsByClassName("checkbox-input");
let tagLabels = document.getElementsByClassName("tag-checkbox");
let numChecked = tagCheckboxes.length;

allCheckbox.addEventListener('click', function() {
    if(allCheckbox.checked){
        for(let i = 0; i < tagCheckboxes.length; i++){
            tagCheckboxes[i].checked = true
            numChecked = tagCheckboxes.length;
        }
    } else {
        for(let i = 0; i < tagCheckboxes.length; i++){
            tagCheckboxes[i].checked = false;
            numChecked = 0;
        }
    }
})
for(let j = 0; j < tagLabels.length; j++){
    let label = tagLabels[j];
    if(label.htmlFor != 'all'){
        label.addEventListener('click', function() {
            if(label.firstElementChild.checked){
                label.firstElementChild.checked = false;
                numChecked--;
            } else {
                label.firstElementChild.checked = true;
                numChecked++;
            }
            if(numChecked >= tagCheckboxes.length && allCheckbox.checked == false){
                allCheckbox.checked = true;
            }
            if(numChecked < tagCheckboxes.length) {
                allCheckbox.checked = false;
            }
        })
    } else {
        label.addEventListener('click', function() {
            if(!allCheckbox.checked){
                for(let i = 0; i < tagCheckboxes.length; i++){
                    tagCheckboxes[i].checked = true
                    numChecked = tagCheckboxes.length;
                }
            } else {
                for(let i = 0; i < tagCheckboxes.length; i++){
                    tagCheckboxes[i].checked = false;
                    numChecked = 0;
                }
            }
        })
    }
}

filterButton.onclick = function() {
    dropdownContent.classList.toggle("showDropdown")
}

window.onclick = function(event) {
    if (!event.target.matches('.dropButton') && !dropdownContent.contains(event.target)) {
        var dropdowns = document.getElementsByClassName("dropdownContent");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('showDropdown')) {
                openDropdown.classList.remove('showDropdown');
            }
        }
    }
}

function filter() {
    let lower, upper;
    if(lowerPrice.value != ''){
        lower = lowerPrice.value
    } else {
        lower = 0
    }
    if(upperPrice.value != ''){
        upper = upperPrice.value
    } else {
        upper = 10000
    }
    let tags=[]
    for(let i = 0; i < tagCheckboxes.length; i++){
        if(tagCheckboxes[i].checked){
            tags.push(tagCheckboxes[i].name);
        }
        else{
            allCheckbox.checked = false;
        }
    }
    if(tags.length == 0){
        tags = ['all']
    }
    fetch(window.location.href, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'selectedTags': tags,
            'lowerPrice': lower,
            'upperPrice': upper,
            'stockAvaliable': stockAvaliable.checked,
        })
    })
    .then(response => response.json())
    .then(data => {
        const productList = document.getElementById("products_avaliable");
        productList.innerHTML = ``;
        if(data.products.length > 0){
            data.products.forEach(product => {
                const listItem = document.createElement("article");
                listItem.innerHTML = `
                <a href="/products/${product.slug}">${product.name}</a>
                <p>R$${product.price}</p>
                `;
                productList.appendChild(listItem);
            });
        } else {
            const notFound = document.createElement("p");
            notFound.innerHTML = "Parece que não há nenhum produto com os filtros aplicados."
            productList.appendChild(notFound);
        }
    })
    .catch(error => console.error('Erro ao carregar dados:', error));
}

productCards.forEach((card) => {
    card.addEventListener('click', function() {
        window.location.href = card.querySelector('a').href;
    })

    card.addEventListener('mouseover', function() {
        card.style.cursor = 'pointer';
    }
    )
    card.addEventListener('mouseout', function() {
        card.style.cursor = 'auto';
    })
})
