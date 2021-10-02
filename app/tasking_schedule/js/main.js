
let beginTimeV,
    addTaskNameInput,
    addTaskSubmit,
    onProgressTaskList,
    completedTaskList;

$(document).ready(() => {
    // init
    beginTimeV = $("#begin-time > span");
    addTaskNameInput = $("#add-task-name-input");
    addTaskSubmit = $("#add-task-submit");
    onProgressTaskList = $("#on-progress-task-list");
    completedTaskList = $("#completed-task-list");
    //
    setBeginTime();
    // listeners
    $("#begin-time-reset").on("click", () => {
        setBeginTime()
    });
    addTaskSubmit.on("click", () => {
        addTask(addTaskNameInput.val());
        addTaskNameInput.val("");
    });
    // event listenters
    addTaskNameInput.keydown((event) => {
        if (event.keyCode === 13 && addTaskNameInput.val() !== "") {
            addTask(addTaskNameInput.val());
            addTaskNameInput.val("");
        }
    });
});

function addTask(name) {
    let taskV = $(`<div class="task on-progress-task"><p>${name}</p></div>`);
    let deleteV = $(`<button class="task-delete-button">delete</button>`);
    taskV.append(deleteV);
    //
    taskV.on("click", () => {
        taskV.remove();
        let completedTaskV = $(`<div class="task completed-task"><p
            style="color: var(--muted-font-color);">${name}</p><span>${getFormattedDate(new Date())}</span></div>`
        );
        completedTaskList.append(completedTaskV);

    });
    deleteV.on("click", () => {
        taskV.remove();
    });
    onProgressTaskList.append(taskV);
}

function setBeginTime() {
    let d = new Date();
    beginTimeV.text(
        getFormattedDate(d)
    );
}
