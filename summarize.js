let summarizeButton = document.getElementById("submitToS");


async function get(url) {
    return fetch(url, {
        method: "GET", 
        headers: {
            "Content-Type": "text/event-stream"
        }
    })
    .then((response) => response.json())
    .catch((erorrMessage) => console.log("Internal error message from script:", erorrMessage));
};



async function fetchSummary() {
    console.log("Button pressed");

    let result = await get("https://tossed-away.vercel.app/summarize");
    console.log(result);
};


summarizeButton.onclick = fetchSummary;
