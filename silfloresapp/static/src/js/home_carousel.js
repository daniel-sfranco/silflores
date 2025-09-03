function setCarousel(elements, numElements, carouselId, urlPrefix, urlSufix) {
    const carousel = document.getElementById(carouselId);
    const innerCarousel = carousel.querySelector(".carousel-inner");

    // Bug 1 Fix: Set the target for the controls to this specific carousel instance
    const prevButton = carousel.querySelector('.carousel-control-prev');
    const nextButton = carousel.querySelector('.carousel-control-next');
    if (prevButton) {
        prevButton.setAttribute('data-bs-target', `#${carouselId}`);
    }
    if (nextButton) {
        nextButton.setAttribute('data-bs-target', `#${carouselId}`);
    }

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
                // Bug 2 Fix: Set data-slug instead of data-name
                card.setAttribute("data-slug", elements[elementCounter].slug);
                card.innerHTML = `
                <img src="${elements[elementCounter].imageUrl}" class="card-img-top" alt="${elements[elementCounter].name} image">
                <div class="card-body">
                    <h5 class="card-title">${elements[elementCounter].name}</h5>
                    <p class="card-text">${elements[elementCounter].desc}</p>
                </div>`;
                card.onclick = function () {
                    // Bug 2 Fix: Use data-slug for the URL
                    let url = card.dataset.slug;
                    if (urlPrefix) {
                        url = urlPrefix + url;
                    }
                    if (urlSufix) {
                        url = url + urlSufix;
                    }
                    window.location.href = url;
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

function setupCarousel(fetchUrl, carouselId, errorMsg, productsKey, numProductsKey) {
    fetch(fetchUrl)
        .then((response) => response.json())
        .then((data) => {
            const products = JSON.parse(data[productsKey]);
            console.log(products);
            const numProducts = data[numProductsKey];
            setCarousel(
                products,
                numProducts,
                carouselId,
                "/products/",
                false
            );
        })
        .catch(error => console.error(errorMsg, error));
}

setupCarousel("/getSoldProducts/", "sold", "Erro ao buscar produtos vendidos:", "soldProducts", "numSoldProducts");
setupCarousel("/getNewProducts/", "new", "Erro ao buscar novos produtos:", "newProducts", "numNewProducts");
