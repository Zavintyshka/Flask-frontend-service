window.addEventListener('scroll', e => {
    document.documentElement.style.setProperty('--scrollTop', `${this.scrollY}px`)
})

window.addEventListener('load', e => {
    if (document.querySelector(".popup_message__title")) {
        show_popup_message()
    }
})

const wrapper_box = document.querySelector(".wrapper_box")
const wrapper_inner = document.querySelector(".wrapper_inner")

// Buttons & Links
const popup_login_btn = document.querySelector("#popup_login_btn")
const close_popup_menu_btn = document.querySelector("#close_popup_menu_btn")
const login_link = document.querySelector("#login_link")
const register_link = document.querySelector("#register_link")

// Forms
const register_form = document.querySelector(".register_form_box")
const login_form = document.querySelector(".login_form_box")

// Init Value
const init_value = function () {
    wrapper_inner.style.height = "500px"
    register_form.style.transform = "translateX(100%)"
    login_form.style.transform = "translateX(0%)"
    register_form.style.display = ""
    login_form.style.display = ""
}

init_value()

const show_popup_menu = function () {
    wrapper_box.style.transform = `scale(1)`
}

const show_login_form = function () {
    wrapper_inner.style.height = "490px"
    switch_form(login_form)
    switch_form(register_form)
}

const show_register_form = function () {
    wrapper_inner.style.height = "650px"
    switch_form(login_form)
    switch_form(register_form)
}

const switch_form = function (form) {
    const is_login = form === login_form
    const edge_value = is_login ? -100 : 100
    const edge = `translateX(${edge_value}%)`
    const center = "translateX(0%)"
    form.style.transform === "translateX(0%)" ? form.style.transform = edge : form.style.transform = center
}

const close_popup_menu = function () {
    init_value()
    wrapper_box.style.transform = "scale(0)"
}


// Event Listeners
if (popup_login_btn) {
    popup_login_btn.addEventListener("click", show_popup_menu)
}
close_popup_menu_btn.addEventListener("click", close_popup_menu)
register_link.addEventListener("click", show_register_form)
login_link.addEventListener("click", show_login_form)


const swiper = new Swiper('.swiper', {
    // Optional parameters
    direction: 'horizontal',
    loop: true,

    // If we need pagination
    pagination: {
        el: '.swiper-pagination',
    },

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    // And if we need scrollbar
    scrollbar: {
        el: '.swiper-scrollbar',
    },
});