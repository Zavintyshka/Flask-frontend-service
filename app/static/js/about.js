const image_cards = document.querySelectorAll(".image_card")
const text_cards = document.querySelectorAll(".text_card")

for (let i = 0; i < image_cards.length; i++) {
    const image_card = image_cards[i]
    const text_card = text_cards[i]
    image_card.addEventListener("mouseenter", () => {
        text_card.classList.add("show")
        image_card.classList.remove("show")
    })
}

for (let i = 0; i < image_cards.length; i++) {
    const image_card = image_cards[i]
    const text_card = text_cards[i]
    text_card.addEventListener("mouseleave", () => {
        image_card.classList.add("show")
        text_card.classList.remove("show")
    })
}



