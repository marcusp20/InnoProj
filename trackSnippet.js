// window.addEventListener('click', function(event) {
//     console.log(event);

// 	updateEvents(event.target, 'click');

//     // Doing nothing in this method lets the event proceed as normal
// }, true // Enable event capturing!
// );

// window.addEventListener('keypress', function(event) {
//     console.log(event);

// 	updateEvents(event.target, 'keypress', event.key);
// });

// function getXPath(element) {
//     // This function generates an XPath expression for a given element

//     // Start with the element itself
//     let xpath = `/${element.tagName.toLowerCase()}`;

//     // If the element has an id attribute, add the id value to the XPath
//     if (element.id) {
//         xpath += `[@id="${element.id}"]`;
//     }// If the element doesn't have an id, add the element's position within its parent to the XPath
//     else {
//         let index = 1;
//         let sibling = element.previousElementSibling;
//         while (sibling) {
//             if (sibling.tagName === element.tagName) {
//                 index++;
//             }
//             sibling = sibling.previousElementSibling;
//         }
//         xpath += `[${index}]`;
//     }

//     // Add the element's ancestors, starting from the parent
//     let parent = element.parentElement;
//     while (parent && parent.tagName !== "HTML") {
//         // Add the parent's position within its parent
//         let index = 1;
//         let sibling = parent.previousElementSibling;
//         while (sibling) {
//             if (sibling.tagName === parent.tagName) {
//                 index++;
//             }
//             sibling = sibling.previousElementSibling;
//         }
//         xpath = `/${parent.tagName.toLowerCase()}[${index}]` + xpath;

//         // Move up to the next ancestor
//         parent = parent.parentElement;
//     }
//     return xpath
// }

// function updateEvents(element, type, key='') {
//     var data = JSON.parse(localStorage.myEvents || '[]');

// 	var xpath = getXPath(element);
// 	if(type == 'keypress' && data.length && data[data.length - 1].type === "keypress")
// 		data[data.length - 1].value += key;
// 	else {
// 		data.push({
// 			type: type,
// 			xpath: xpath,
// 			value: key
// 		});
// 	}

//     localStorage.myEvents = JSON.stringify(data);
// }

javascript: (function () {
    window.addEventListener('click', function (event) {
        console.log(event);

        updateEvents(event.target, 'click');

    }, true
    );

    window.addEventListener('keypress', function (event) {
        console.log(event);

        updateEvents(event.target, 'keypress', event.key);
    });

    function getXPath(element) {
        let xpath = `/${element.tagName.toLowerCase()}`;

        if (element.id) {
            xpath += `[@id="${element.id}"]`;
        }
        else {
            let index = 1;
            let sibling = element.previousElementSibling;
            while (sibling) {
                if (sibling.tagName === element.tagName) {
                    index++;
                }
                sibling = sibling.previousElementSibling;
            }
            xpath += `[${index}]`;
        }

        let parent = element.parentElement;
        while (parent && parent.tagName !== "HTML") {
            let index = 1;
            let sibling = parent.previousElementSibling;
            while (sibling) {
                if (sibling.tagName === parent.tagName) {
                    index++;
                }
                sibling = sibling.previousElementSibling;
            }
            xpath = `/${parent.tagName.toLowerCase()}[${index}]` + xpath;

            parent = parent.parentElement;
        }
        return xpath
    }

    function updateEvents(element, type, key = '') {
        var data = JSON.parse(localStorage.myEvents || '[]');

        var xpath = getXPath(element);
        if (type == 'keypress' && data.length && data[data.length - 1].type === "keypress")
            data[data.length - 1].value += key;
        else {
            data.push({
                type: type,
                xpath: xpath,
                value: key
            });
        }

        localStorage.myEvents = JSON.stringify(data);
    }
})();

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

javascript: (function () {
    localStorage.myEvents = [];
})();