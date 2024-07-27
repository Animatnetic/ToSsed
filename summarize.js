let summarizeButton = document.getElementById("submitToS");


async function get(url) {
    return fetch(url, {
        method: "GET", 
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then((response) => response.json())
    .catch((erorrMessage) => console.log("Internal error message from script:", erorrMessage));
};


async function post(url) {
    return fetch(url, {
        method: "POST", 
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then((response) => response.json())
    .catch((erorrMessage) => console.log("Internal error message from script:", erorrMessage));
};


async function fetchSummary() {
    console.log("Button pressed");

    let result = await post("https://tossed-away.vercel.app/summarize");
    console.log(result);
};


summarizeButton.onclick = fetchSummary;
