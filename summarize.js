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
    summarizeButton.disabled = true;
    console.log("Button pressed");

    let loadingElement = document.createElement("div");
    loadingElement.innerHTML = 
    `
        <div>
            <div class="spinner-border spinner-border-sm fs-3 m-1" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    summarizeButton.appendChild(loadingElement);

    let result = await get(`https://tossed-away.vercel.app/summarize?input=${inputtedText.value}`);
    
    // Allow the button to be pressed again, and remove the loading after the data has been retreived 
    summarizeButton.removeChild(loadingElement);
    summarizeButton.disabled = false;
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
