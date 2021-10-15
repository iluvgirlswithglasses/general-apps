
function handleUpdated(tabId, changeInfo, tabInfo) {

    var tabUpdated = false;

    console.log(tabId);
    console.log(changeInfo);
    console.log(tabInfo);

    if (changeInfo.status == "loading" && changeInfo.url == "about:privatebrowsing"){
        //console.log("opening about:blank..");
        browser.tabs.update(tabId, {url: "about:blank", active: true});
        tabUpdated = true;
    } else if (
        tabInfo.favIconUrl == "chrome://browser/skin/privatebrowsing/favicon.svg" &&
            tabInfo.incognito == true &&
            tabInfo.url == "about:blank"
    ){
        browser.tabs.update(tabId, {url: "about:blank", active: true});
        tabUpdated = true;
    }

    if (tabInfo.status == "complete" && tabUpdated) {
        browser.tabs.reload(tabId, {bypassCache: true});
    }
}

browser.tabs.onUpdated.addListener(handleUpdated);
