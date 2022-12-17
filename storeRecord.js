javascript: (function () {
    console.log(JSON.stringify(localStorage.myEvents));

    fetch("http://localhost:8000/", {
        method: "POST",
        body: JSON.stringify(localStorage.myEvents),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(json => console.log(json));
})();