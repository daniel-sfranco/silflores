function setCarousel(elements, numElements, carouselId, urlPrefix, urlSufix) {
    const carousel = document.getElementById(carouselId);
    const innerCarousel = carousel.querySelector(".carousel-inner");
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
                <img src="${elements[elementCounter].imageUrl}" class="card-img-top" alt="${elements[elementCounter].name} image">
                <div class="card-body">
                    <h5 class="card-title">${elements[elementCounter].name}</h5>
                    <p class="card-text">${elements[elementCounter].desc}</p>
                </div>`;
                card.onclick = function () {
                    console.log(card.dataset.name);
                    let url = card.dataset.name;
                    if (urlPrefix) {
                        url = urlPrefix + url;
                    }
                    if (urlSufix) {
                        url = url + urlSufix;
                    }
                    window.location.href = url.toLowerCase();
                };
                actElement.appendChild(card);
                innerRow.appendChild(actElement);
                elementCounter++;
            }
        }
        innerCarousel.appendChild(actRow);
    }
    if(numElements <= elementsPerRow){
        const prev = carousel.querySelector('.carousel-control-prev')
        const next = carousel.querySelector('.carousel-control-next')
        prev.setAttribute("style", "display: none")
        next.setAttribute("style", "display: none")
    }
}

let soldProducts = 0;
let numSoldProducts = 0;
fetch("/getSoldProducts/")
.then((response) => response.json())
.then((data) => {
    soldProducts = JSON.parse(data.soldProducts);
    numSoldProducts = data.numSoldProducts;
    setCarousel(
        soldProducts,
        numSoldProducts,
        "sold",
        "/products/",
        false
    );
});

let newProducts = 0;
let numNewProducts = 0;
fetch("/getNewProducts/")
.then((response) => response.json())
.then((data) => {
    newProducts = JSON.parse(data.newProducts);
    numNewProducts = data.numNewProducts;
    setCarousel(
        newProducts,
        numNewProducts,
        "new",
        "/products/",
        false
    );
});