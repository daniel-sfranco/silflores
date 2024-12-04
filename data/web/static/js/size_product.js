const typeField = document.getElementById("id_size_type")
const typeHelp = document.getElementById("id_size_helptext")
typeHelp.style.display = "none"

typeField.addEventListener('change', function() {
    if(typeField.value == 'choice'){
        typeHelp.style.display = "flex"
    } else {
        typeHelp.style.display = "none"
    }
})