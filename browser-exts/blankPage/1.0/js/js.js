
let paras = [
        $("#clock-hr"),
        $("#clock-min"),
        $("#clock-sec"),
    ],
    datePara = $("#date"),
    times = [],
    weekdays = [    // index 0 is Sunday (not Monday like Python)
        "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    ],
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December',
    ];

$(document).ready(() => {
    initial();
});

function initial() {
    let i = new Date();
    times = [
        i.getHours(),
        i.getMinutes(),
        i.getSeconds(),
    ];
    let shiftMillisec = 1000 - i.getMilliseconds();
    updateClock();
    updateDate();
    setTimeout(function () {
        timeInterval();
        setInterval(timeInterval, 1000)
    }, shiftMillisec)
}

function timeInterval() {
    times[2] += 1;
    timesCondition();
    updateClock();
}

function timesCondition() {
    if (times[2] === 60) {  // sec to min
        times[2] = 0;
        times[1] += 1;
        if (times[1] === 60) {  // min to hr
            times[1] = 0;
            times[0] += 1;
            if (times[0] === 24) {  // hr to date
                times[0] = 0;
                updateDate();
            }
        }
    }
}

function updateClock() {
    for (let i in times) {
        let str = times[i].toString();
        paras[i].text("0".repeat(2-str.length) + str);
    }
}

function updateDate() {
    let i = new Date();
    let weekday = weekdays[i.getDay()],
        day = i.getDate(),
        month = months[i.getMonth()],
        year = i.getFullYear();
    datePara.html(`<span>${weekday}</span>, ${month} ${day} ${year}`);
}

