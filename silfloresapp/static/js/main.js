const searchInput = document.getElementById('product-search')
const searchButton = document.getElementById('search-button')
const csrftoken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

function search() {
    if(searchInput.value){
        window.location.href = `/products/all/list/${searchInput.value}`
    }
}

searchInput.addEventListener('keypress', function(e) {
    if(e.key === 'Enter'){
        search()
    }
})
