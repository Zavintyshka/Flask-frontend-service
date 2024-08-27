burger_menu_button = document.querySelector(".burger_menu_button")
burger_menu_tab = document.querySelector(".burger_menu_tab")
second_page_link = document.querySelector(".second_page_link")
burger_login_button = document.querySelector("#navigation__login_button")


window.addEventListener("resize", () => {
    if (window.innerWidth > 1085) {
        burger_menu_tab.style.top = "-190px";
    }
})


const switch_burger_menu = () => {
    const height_state = burger_menu_tab.style.top
    const is_open = height_state === "0px";
    if (is_open) {
        burger_menu_tab.style.top = "-190px";
    } else {
        burger_menu_tab.style.top = "0px";
    }
}

burger_menu_button.addEventListener("click", switch_burger_menu)
second_page_link.addEventListener("click", switch_burger_menu)
burger_login_button.addEventListener("click", () => {
    switch_burger_menu();
    popup_login_btn.click();
})



