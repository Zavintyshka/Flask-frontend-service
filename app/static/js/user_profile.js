const cards = document.querySelectorAll(".user_achievements__card")
const progress_bars = document.querySelectorAll(".achievement_progress_bar")
const user_progress = document.querySelectorAll(".user_achievements__description__progress")

for (let index = 0; index < cards.length; index++) {
    const card = cards[index]
    const progress_bar = progress_bars[index]
    const [progress, target] = user_progress[index].textContent.split("/").map(Number)
    const progress_bar_line = progress_bar.querySelector(".achievement_progress_bar__progress")

    progress_bar_line.style.width = `${progress / target * 100}%`


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



