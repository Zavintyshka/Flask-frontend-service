const download_buttons = document.querySelectorAll(".download_button")

const jwt_token = document.cookie.split("jwt_token=")[1]

const download_file = (url, downloading_filename) => {
    fetch(url, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${jwt_token}`
        }
    }).then(response => {
        if (!response.ok) {
            return alert(`Something went wrong. Status: ${response.status}`)
        }
        return response.blob()
    }).then(data => {
            const url = URL.createObjectURL(data);
            const anchor = document.createElement("a");
            anchor.href = url;
            anchor.download = downloading_filename;
            anchor.style.display = "none";
            document.body.append(anchor)
            anchor.click();
            anchor.remove();
        }
    )
}


for (let i = 0; i < download_buttons.length; i++) {
    const download_button = download_buttons[i];
    const parent = download_button.parentElement.parentElement;
    const filename = parent.querySelector(".part_filename").querySelector("h4").textContent
    const download_link = download_button.getAttribute("download_link");
    download_button.addEventListener("click", () => {
        download_file(download_link, filename)
    })
}