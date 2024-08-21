const reset_password_button = document.querySelector(".reset_password_button")
const popup_message = document.querySelector(".popup_message")

const text = document.querySelector(".popup_message__text")
const add_text = document.querySelector(".popup_message__add_text")
const form = document.querySelector(".form_wrapper")

form.addEventListener("submit", (event) => {
    event.preventDefault()
    const form_data = new FormData(form)
    fetch("http://192.168.0.176:8000/email/reset-password/", {
            method: "POST",
            body: form_data
        }
    ).then(response => {
        if (response.status === 200 || 404) {
            text.textContent = "If the provided information is correct, a password reset instruction has been sent to the specified email address."
            add_text.textContent = "After 10 seconds, you will be redirected to the main page."
        } else {
            text.textContent = "Something went wrong. Try again later."
        }
        popup_message.classList.add("popup_message-active")
    })
})
