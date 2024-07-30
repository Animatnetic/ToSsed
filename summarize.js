// Elements are using bootstrap v5.3

let summarizeButton = document.getElementById("submitToS");
let inputtedText = document.getElementById("inputTextField");
let warningModal = document.getElementById("warningModal");

let summarizeSection = document.querySelector("section");

let accordianDivContainer = document.createElement("div");
accordianDivContainer.setAttribute("class", "accordion");
accordianDivContainer.setAttribute("id", "outputAccordion");

let gradeElement = document.createElement("div");
gradeElement.setAttribute("class", "alert alert-light");
gradeElement.setAttribute("role", "alert");

let alertElement = document.createElement("div");
alertElement.setAttribute("class", "alert alert-warning d-flex");
alertElement.setAttribute("style", "justify-content: center;");
alertElement.setAttribute("role", "alert");
alertElement.innerText = " Keep in mind, this is an artifical intelligent model so summaries or grading may be incorrect.";


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


function chooseGradeColor(gradeText) {
    if (gradeText == "A") {
        return "success";
    } else if (gradeText == "B") {
        return "primary";
    } else if (gradeText == "C") { 
        return "info";
    } else if (gradeText == "D") {
        return "warning";
    } else if (gradeText == "E") {
        return "danger";
    } else {
        return "secondary";
    };
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
    console.log(result);
    
    // Allow the button to be pressed again, and remove the loading after the data has been retreived 
    summarizeButton.removeChild(loadingElement);
    summarizeButton.disabled = false;

    summarizeSection.appendChild(accordianDivContainer);

    for (let summaryPointIndex = 0; summaryPointIndex < result["all_summaries"].length; summaryPointIndex ++) {
        // String template for creating accordian elements in a programmatic manner
        let accordianIdentifier = `collapse${summaryPointIndex}` // Uniquely identify each accordian element

        let accordianElement = 
        `
        <div class="accordion-item">
            <h2 class="accordion-header">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#${accordianIdentifier}" aria-expanded="false" aria-controls="#${accordianIdentifier}">
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

        accordianDivContainer.insertAdjacentHTML("beforeend", accordianElement);
    };


    let grade = result["grade"]

    let clonedGradeElement = gradeElement.cloneNode();
    clonedGradeElement.innerHTML = 
    `
    <div class="fw-bold">
        Grade: <span class="badge text-bg-${chooseGradeColor(grade)}">${grade}</span>
    </div>
    `;// class="text-bg-[variable colour depending on grade]"

    let clonedAlertElement = alertElement.cloneNode();

    accordianDivContainer.insertAdjacentElement("beforeend", gradeElement);
    accordianDivContainer.insertAdjacentElement("beforeend", clonedAlertElement);
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
