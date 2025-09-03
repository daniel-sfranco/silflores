function setCarousel(elements, numElements, carouselId) {
    const innerCarousel = document.getElementById(carouselId);
    const width = window.screen.width;
    let elementsPerRow = 4;
    if (width < 576) {
        elementsPerRow = 2;
    } else if (width < 992) {
        elementsPerRow = 3;
    }
    let elementCounter = 0;
    while (elementCounter < numElements) {
        const actRow = document.createElement("div");
        actRow.setAttribute("class", "carousel-item");
        if (elementCounter == 0) {
            actRow.setAttribute("class", "carousel-item active");
        }
        const innerRow = document.createElement("div");
        innerRow.setAttribute("class", "row");
        actRow.appendChild(innerRow);
        for (let j = 0; j < elementsPerRow; j++) {
            if (elementCounter < numElements) {
                const actElement = document.createElement("div");
                actElement.setAttribute(
                    "class",
                    "col-lg-3 col-md-4 col-sm-4 col-6"
                );
                actElement.setAttribute("style", `order: ${elementCounter}`);
                const card = document.createElement("div");
                card.setAttribute("class", "card");
                card.setAttribute("data-name", elements[elementCounter].name);
                card.innerHTML = `
                <img src="${elements[elementCounter].photoUrl}" class="card-img-top" alt="${elements[elementCounter].label} image" data-delete-url="/products/photo/${elements[elementCounter].label}/delete">`;
                actElement.appendChild(card);
                innerRow.appendChild(actElement);
                elementCounter++;
            }
        }
        innerCarousel.appendChild(actRow);
    }
    if(numElements <= elementsPerRow){
        const prev = document.getElementById('prev-photo-button')
        const next = document.getElementById('next-photo-button')
        prev.setAttribute("style", "display: none")
        next.setAttribute("style", "display: none")
    }
}

let photos = [];
let numPhotos = 0;

fetch(`/products/getProductJson/${data.getAttribute('data-slug')}`)
.then(response => response.json())
.then(data => {
    photos = data.photos;
    numPhotos = data.numPhotos;
    setCarousel(
        photos,
        numPhotos,
        "photo-carousel",
    );
})
.catch(error => console.error('Erro ao buscar fotos do produto:', error));
