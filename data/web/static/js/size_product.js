const typeField = document.getElementById("id_size_type")
const typeHelp = document.getElementById("id_size_helptext")
const sizeField = document.getElementById("id_size")
const sizeHelp = document.getElementById("")
typeHelp.style.display = "none"

typeField.addEventListener('change', function() {
    if(typeField.value == 'choice'){
        typeHelp.style.display = "flex"
    } else if(typeField.value == 'fixed'){
        typeHelp.style.display = "none"
    } else {
        typeHelp.textContent = "Deixe esse campo em branco"
    }
})