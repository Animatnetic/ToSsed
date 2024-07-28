let summarizeButton = document.getElementById("submitToS");
let inputtedText = document.getElementById("inputTextField");


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

    let result = await get(`https://tossed-away.vercel.app/summarize?input=${inputtedText.value}`);
    console.log(result);
};


summarizeButton.onclick = fetchSummary;
