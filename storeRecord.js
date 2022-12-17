javascript: (function () {
    console.log(JSON.stringify(localStorage.myEvents));

    if(!localStorage.myEvents.length){
        return;
    }

    fetch("http://localhost:8000/", {
        method: "POST",
        body: JSON.stringify(localStorage.myEvents[0]),
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        console.log(response);
        localStorage.
    });
})();