const jwt_token = document.cookie.split("jwt_token=")[1]

// drag & drop area
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


const form_data = new FormData();

const get_formatted_time = (raw_seconds) => {
    const total_seconds = Math.floor(raw_seconds);
    const minutes = Math.floor(total_seconds / 60);
    const seconds = (total_seconds % 60).toString().padStart(2, "0");
    return `${minutes}:${seconds}`
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
    start_time.setAttribute("time", time)
    start_time.textContent = get_formatted_time(time);
})
set_end_time_button.addEventListener("click", () => {
    const time = videoplayer.currentTime
    end_time.setAttribute("time", time)
    end_time.textContent = get_formatted_time(time);
})
cut_submit_button.addEventListener("click", () => {
    form_data.append("action", "cut");
    form_data.append("start_time", start_time.getAttribute("time"));
    form_data.append("end_time", end_time.getAttribute("time"));
    send_video();
})


const upload_video = (file) => {
    form_data.append("file", file)
    form_data.append("filename", file.name)
    filename.textContent = file.name;
    videoplayer.src = URL.createObjectURL(file);
    video_wrapper.style.height = "1500px"
}


const send_video = () => {
    console.log(form_data)
    fetch("http://192.168.0.176:5050/video", {
            method: "POST",
            credentials: "include",
            body: form_data
        }
    ).then(response => {
        if (!response.ok) {
            return alert(`Something went wrong. Status: ${response.status}`)
        }
        window.location.href="http://192.168.0.176:5050/"
    })
}