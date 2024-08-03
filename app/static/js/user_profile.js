const cards = document.querySelectorAll(".user_achievements__card")


for (let index = 0; index < cards.length; index++) {
    const card = cards[index]
    card.addEventListener("mousemove", (event) => {
        const rect = card.getBoundingClientRect();

        const width = rect.width;
        const height = rect.height;

        const mid_x = width / 2;
        const mid_y = height / 2;
        const raw_x = event.clientX - rect.left;
        const raw_y = event.clientY - rect.top;

        const x = (raw_x - mid_x) / 6;
        const y = (raw_y - mid_y) / -4;

        Object.assign(document.documentElement, {
            style: `--move-x: ${x}deg; --move-y: ${y}deg;`
        })
    })

    card.addEventListener('mouseleave', () => {
        Object.assign(document.documentElement, {
            style: `--move-x: 0deg; --move-y: 0deg;`
        })
    });
}



