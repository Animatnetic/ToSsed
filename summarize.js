// Elements are using bootstrap v5.3

let summarizeButton = document.getElementById("submitToS");
let inputtedText = document.getElementById("inputTextField");
let warningModal = document.getElementById("warningModal");

let summarizeSection = document.querySelector("section");

let accordianDivContainer = document.createElement("div");
accordianDivContainer.setAttribute("class", "accordian");
accordianDivContainer.setAttribute("id", "outputAccordian");

let gradeElement = document.createElement("div");
gradeElement.setAttribute("class", "alert alert-light");
gradeElement.setAttribute("role", "alert");
gradeElement.innerHTML = 
`
<div class="fw-bold">
    Grade: <span class="badge"></span>
</div>
`;// class="text-bg-[variable colour depending on grade]"

let alertElement = document.createElement("div");
alertElement.setAttribute("class", "alert alert-warning d-flex");
alertElement.setAttribute("style", "justify-content: center;");
alertElement.setAttribute("role", "alert");
alertElement.innerHTML = " Keep in mind, this is an artifical intelligent model so summaries or grading may be incorrect.";


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


async function post(url, payload) {
    return fetch(url, {
        method: "POST",
        body: payload,
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then((response) => response.json())
    .catch((erorrMessage) => {
        console.log("Internal error message from script:", erorrMessage);
        alert("An unexpected error occured!");
    });
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
    `; // HTML for the loading screen
    summarizeButton.appendChild(loadingElement);

    let result = await post("https://tossed-away.vercel.app/summarize", inputtedText.value);
    
    // Allow the button to be pressed again, and remove the loading after the data has been retreived 
    summarizeButton.removeChild(loadingElement);
    summarizeButton.disabled = false;

    for (let summaryPointIndex = 0; summaryPointIndex <= result["all_summaries"].length; summaryPointIndex ++) {
        // String template for creating accordian elements in a programmatic manner
        let accordianIdentifier = `collapse${summaryPointIndex}` // Uniquely identify each accordian element

        let accordianElementTemplate = 
        `
        <div class="accordion-item">
            <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" aria-expanded="false" data-bs-target="${accordianIdentifier}" aria-controls="${accordianIdentifier}">
            ${result["all_summaries"][summaryPointIndex]["summary_title"]}
            </button>
            </h2>
            <div id="${accordianIdentifier}" class="accordion-collapse collapse">
            <div class="accordion-body">
            ${result["all_summaries"][summaryPointIndex]["summary_meaning"]}
            </div>
            </div>
        </div>
        `;
// Do note, I set the data-bs-controls and aria-controls programmatically 

        accordianDivContainer.appendChild(accordianElementTemplate);
    };
};


summarizeButton.onclick = fetchSummary;

inputtedText.addEventListener("input", () => {
    console.log("Input logged");

    if (inputtedText.value == "") {
        summarizeButton.setAttribute("data-bs-toggle", "modal");
        summarizeButton.setAttribute("data-bs-target", "#warningModal");
    } else {
        summarizeButton.removeAttribute("data-bs-toggle", "modal");
        summarizeButton.removeAttribute("data-bs-target", "#warningModal");
    };
    // Warning the user for if they summarize a blank input as to not waste AI computation
});
