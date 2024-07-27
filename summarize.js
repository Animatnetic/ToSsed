let summarizeButton = document.getElementById("submitToS");


async function get(url) {
    return fetch(url, {
        method: "GET"
    })
    .then((response) => response.json());
};



async function fetchSummary() {
    console.log("Button pressed");

    let result = await get("https://tossed-away.vercel.app/summarize");
    console.log(result);
};


summarizeButton.onclick = fetchSummary;
