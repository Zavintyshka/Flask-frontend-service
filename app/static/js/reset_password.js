const form = document.querySelector(".form_wrapper")
form.addEventListener("submit", (event) => {
    event.preventDefault()
    const form_data = new FormData(form)
    fetch("http://192.168.0.176:8000/email/reset-password/", {
            method: "POST",
            body: form_data
        }
    ).then(response => {
        if (response.status === 200) {
            set_popup_message("If the provided information is correct, a password reset instruction has been sent to the specified email address.")
            const button = form.querySelector(".reset_password_button")
            button.classList.add("disabled")
        } else {
            set_popup_message("Something went wrong. Please try again later.")
        }
        show_popup_message()
    })
})
