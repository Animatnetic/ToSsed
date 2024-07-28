let summarizeButton = document.getElementById("submitToS");
let inputtedText = document.getElementById("inputTextField");
let warningModal = document.getElementById("warningModal");


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

inputtedText.addEventListener("input", () => {
    console.log("Input logged");

    // data-bs-="modal" data-bs-target="#warningModal"

    if (inputtedText.value == "") {
        summarizeButton.setAttribute("data-bs-toggle", "modal");
        summarizeButton.setAttribute("data-bs-target", "#warningModal");
    } else {
        summarizeButton.removeAttribute("data-bs-toggle", "modal");
        summarizeButton.removeAttribute("data-bs-target", "#warningModal");
    };
});
