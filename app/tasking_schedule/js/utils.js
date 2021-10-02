
function getFormattedDate(d) {
    return `${
            getLeadingZero(d.getHours(), 2)
        }h${
            getLeadingZero(d.getMinutes(), 2)
        }m${
            getLeadingZero(d.getSeconds(), 2)
        }s`;
}

function getLeadingZero(n, len) {
    let str = "" + n;
    while (str.length < len) str = "0" + str;
    return str;
}
