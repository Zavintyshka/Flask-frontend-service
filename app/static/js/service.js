const jwt_token = document.cookie.split("jwt_token=")[1]

// drag & drop area
const drag_area_wrapper = document.querySelector(".drag_and_drop_area_wrapper");
const drag_area = document.querySelector(".drag_and_drop_area");
const description = drag_area.querySelector(".drag_and_drop_area__description")
const input_field = drag_area.querySelector("#video_file")


// video player
const video_wrapper = document.querySelector(".video_block__wrapper")
const videoplayer = document.querySelector("#videoplayer")
const filename = document.querySelector(".video_block__title")

// actions

// 1. cut
const set_start_time_button = document.querySelector(".cut_action__set_start_time")
const set_end_time_button = document.querySelector(".cut_action__set_end_time")
const start_time = document.querySelector(".cut_action__start_time")
const end_time = document.querySelector(".cut_action__end_time")
const cut_submit_button = document.querySelector(".cut_action__submit_button")


// 2. Convert
const convert_submit_button = document.querySelector(".convert_action__submit_button")
const file_ext_field = document.querySelector(".convert_action__file_ext_from")
const drop_down_menu = document.querySelector("#file_ext_list")
file_ext_field.textContent = getFileExtension(filename.textContent)


const form_data = new FormData();

function getFileExtension(filename) {
    const dotIndex = filename.lastIndexOf('.');
    return dotIndex !== -1 ? filename.slice(dotIndex + 1) : '';
}


const get_formatted_time = (raw_seconds) => {
    const ms = Math.floor((raw_seconds % 1 * 1000)).toString().padStart(2, "0")
    const total_seconds = Math.floor(raw_seconds)
    const hours = Math.floor(total_seconds / 3600).toString().padStart(2, "0")
    const minutes = Math.floor(total_seconds % 3600 / 60).toString().padStart(2, "0")
    const seconds = (total_seconds % 60).toString().padStart(2, "0")

    return [`${minutes}:${seconds}`, `${hours}:${minutes}:${seconds}.${ms}`]
}

// drag & drop area
drag_area.addEventListener("click", () => {
    input_field.click();
    input_field.onchange = (e) => {
        upload_video(e.target.files[0])
    }
})
drag_area.addEventListener("dragover", (e) => {
    e.preventDefault();
    drag_area.style = "border: 4px solid black;"
});
drag_area.addEventListener("dragleave", (e) => {
    e.preventDefault();
    drag_area.style = "border: 4px dashed black;"
});
drag_area.addEventListener("drop", (e) => {
    e.preventDefault();
    if (e.dataTransfer.items[0].kind !== "file") {
        description.textContent = "Unsupported File"
        throw new Error("Unsupported File");
    }


    if (e.dataTransfer.items.length !== 1) {
        description.textContent = "Too many files were given"
        throw new Error("Too many files were given");
    }

    upload_video(e.dataTransfer.files[0]);
});


// cut action
set_start_time_button.addEventListener("click", () => {
    const time = videoplayer.currentTime
    const formatted_times = get_formatted_time(time)
    start_time.setAttribute("time", formatted_times[1])
    start_time.textContent = formatted_times[0];
})
set_end_time_button.addEventListener("click", () => {
    const time = videoplayer.currentTime
    const formatted_times = get_formatted_time(time)
    end_time.setAttribute("time", formatted_times[1])
    end_time.textContent = formatted_times[0];
})
cut_submit_button.addEventListener("click", () => {
    form_data.append("action_type", "cut");
    const file_ext = getFileExtension(filename.textContent)
    form_data.append("action", `${file_ext};${file_ext};${start_time.getAttribute("time")};${end_time.getAttribute("time")}`);
    send_video();
})

// convert action
convert_submit_button.addEventListener("click", () => {
    form_data.append("action_type", "convert");
    const file_ext = getFileExtension(filename.textContent)
    const convert_to_ext = drop_down_menu.value.toLowerCase()
    console.log(convert_to_ext)
    form_data.append("action", `${file_ext};${convert_to_ext}`);
    send_video();
})

const upload_video = (file) => {
    form_data.append("file", file)
    form_data.append("filename", file.name)
    filename.textContent = file.name;
    file_ext_field.textContent = getFileExtension(file.name)
    videoplayer.src = URL.createObjectURL(file);
    drag_area_wrapper.classList.add("drag_and_drop_area_wrapper-disabled")
    video_wrapper.classList.remove("video_block__wrapper-disabled")
    preload_video()
}


const preload_video = () => {
    fetch("http://192.168.0.176:5050/preload/", {
        method: "POST",
        credentials: "same-origin",
        body: form_data
    }).then(response => {
        if (response.ok) {
            console.log("success")
        } else {
            console.log("something went wrong")
        }
    })
}

const send_video = () => {
    fetch("http://192.168.0.176:5050/video/", {
        method: "POST",
        credentials: "same-origin",
        body: form_data
    }).then(response => {
        if (response.ok) {
            console.log("success")
            window.location.href = "/"
        } else {
            console.log("Something went wrong")
        }
    })
}