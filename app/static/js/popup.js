const popup_box = document.querySelector(".popup_message_box")
const show_popup_message = () => {
    popup_box.classList.add("show")
    setTimeout(() => {
        popup_box.classList.remove("show")
    }, 4000)
    popup_box.getElementsByTagName("li")
}


const set_popup_message = (message) => {
    if (popup_box.querySelector("li")) {
        const li = popup_box.querySelector("li")
        li.textContent = message

    } else {
        const ul = document.createElement("ul")
        const main_text = document.createElement("li")
        main_text.innerText = message
        ul.appendChild(main_text)
        popup_box.appendChild(ul)
    }
}