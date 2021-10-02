let // calculating variables
    moving = 0, timers = [0, 0], timerObject = null,
    firstMove = 0, timeLimit = 3000,
    // disp
    dispTimers = [
        [$("#frame-0"), $("#clock-0")],
        [$("#frame-1"), $("#clock-1")]
    ],
    dispClocks = [
        [$("#min-0"), $("#sec-0")],
        [$("#min-1"), $("#sec-1")],
    ],
    // toolbar
    stopBt = $("#timer-off"),
    settingsBt = $("#setting-bt"), settingsBox = $("#settings-box"),
    // settingsBox's inner
    inpTimeLimit = $("#time-limit-min"),
    inpFirstMove = $("#first-move"),
    // others
    colorSet = {
        "onturn-fg": "#222222",
        "onturn-bg": "#d2d421",
        "offturn-fg": "#ffffff",
        "offturn-bg": "#444444",
    },
    guide = $("#guide");

// on start
settingsBox.hide();
$(document).ready(() => {
    // loading screen
    $("#loading-scene").remove();
    // toolbar
    stopBt.on("click", () => onRestart());
    inpTimeLimit.val(5);
    // settings
    offSettings();
    inpTimeLimit.on("change textInput input", () => {
        let val = Number(inpTimeLimit.val());
        // eliminate spcs case
        if (val <= 0) {
            val = 5;
        } else if (val > 15) {
            val = 15;
        } else if (val % 1 !== 0) {
            val = parseInt(val);
        }
        // applying
        inpTimeLimit.val(val);
        timeLimit = val * 600;
        apply();
        return
    });
    inpTimeLimit.on("click", () => {inpTimeLimit.select()})
    inpFirstMove.on("click", () => {
        let newVal = (Number(inpFirstMove.val()) + 1) % 2;
        inpFirstMove.val(newVal);
        inpFirstMove.text(["Left", "Right"][newVal]);
        firstMove = newVal;
        apply();
        onSwap();
    })
    // others
    initialize();
})

// space command handler
function bindSpace(func) {
    $("#container").on("click", () => {
        func()
    });
    $(document).keypress((event) => {
        if (event.keyCode == 32) {
            func()
        }
    })
}

function clearSpace() {
    $("#container").unbind();
    $(document).unbind();
}

function bindStart() {
    bindSpace(function () {
        clearSpace();;
        // calculating vars
        timerObject = setInterval(executeTimer, 100);
        moving = (moving + 1) % 2;
        onSwap();
        // elements changes
        settingsBt.hide();
        stopBt.show();
        guide.fadeOut();
        // moves
        bindSwap();
    })
}

function bindSwap() {
    bindSpace(function () {
        timers[moving] += 20;
        updateDisp(parseInt(timers[moving]/10), moving);
        moving = (moving + 1) % 2;
        onSwap();
    })
}

function bindRestart() {
    bindSpace(function () {
        initialize();
        guide.html("Press <span>[Space]</span> to start !");
    })
}

function onSettings() {
    // global handlers
    clearSpace();
    guide.html("Press <span>[Space]</span> to close Settings");
    bindSpace(function () {
        offSettings();
        bindStart();
    })
    // clear previous settings' behaviors
    settingsBox.stop(); settingsBt.unbind();
    // works on settings
    settingsBox.slideDown();
    settingsBt.text("Close Settings");
    settingsBt.on("click", () => {
        offSettings();
        bindStart();
    })
}

function offSettings() {
    guide.html("Press <span>[Space]</span> to start !")
    settingsBox.stop(); settingsBt.unbind();
    settingsBox.slideUp();
    settingsBt.text("Settings");
    settingsBt.on("click", () => {
        onSettings();
    });
}

function onSwap() {
    dispTimers[moving][0].css("background-color", colorSet["onturn-bg"]);
    dispTimers[moving][1].css("color", colorSet["onturn-fg"]);
    let offside = (moving + 1) % 2;
    dispTimers[offside][0].css("background-color", colorSet["offturn-bg"]);
    dispTimers[offside][1].css("color", colorSet["offturn-fg"]);
}

function onRestart() {
    // calculating things
    clearInterval(timerObject);
    guide.html("Press <span>[Space]</span> to start !")
    guide.fadeIn();
    initialize();
}

// calculating functions
function executeTimer() {
    let time = timers[moving] - 1, timeSec = (time / 10) - (time / 10) % 1;
    timers[moving] = time;
    if (timeSec % 1 == 0) {
        updateDisp(timeSec, moving);
    }
    if (time == 0) {
        clearInterval(timerObject);
        guide.fadeIn();
        guide.html("Press <span>[Space]</span> to restart !");
        // bindings
        clearSpace();
        bindRestart();
    }
}

// moderating functions
function updateDisp(timeSec, turn) {
    let sec = timeSec % 60, min = (timeSec - sec)/60,
        secString = sec.toString();
    dispClocks[turn][0].text(min);
    if (secString.length === 1) {
        dispClocks[turn][1].text("0" + secString);
    } else {
        dispClocks[turn][1].text(secString);
    }
}

function initialize() {
    // unbindings
    clearSpace();
    // toolbar
    stopBt.hide(); settingsBt.show();
    // moves
    apply();
    bindStart();
}

function apply() {
    // turning
    moving = firstMove;
    // timing
    timers = [timeLimit, timeLimit];
    updateDisp(timeLimit/10, 0); updateDisp(timeLimit/10, 1);
    onSwap();
}
