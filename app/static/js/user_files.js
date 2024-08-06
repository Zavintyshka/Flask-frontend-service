const download_buttons = document.querySelectorAll(".download_button")
const jwt_token = document.cookie.split("jwt_token=")[1]

for (let i = 0; i < download_buttons.length; i++) {
    const download_button = download_buttons[i];
    const download_link = download_button.getAttribute("download_link");

    download_button.addEventListener("click", () => {
        fetch(download_link, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${jwt_token}`
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch the file. Status: " + response.status);
                }
                return response.blob();
            })
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'downloaded-file';
                document.body.appendChild(a);
                a.click();
                URL.revokeObjectURL(url);
            })
            .catch(error => {
                console.error("Error:", error);
                alert(error);
            });
    });
}