/**
 * These functions can be implemented as individual bookmarklets, by
 */

/**
 * X-Path Recorder
 * Bookmarklet that records what the elements user interacts on a website.
 *
 * All comments must be encapsulated by multi-line comments
 * since the script needs to be a "one-liner" in the bookmarklet.
 */
(function () {
    if(window.hasAddedEventListener){
        return;
    }
    /* Set up a click event listener on the window. */
    window.addEventListener('click', function (event) {
        console.log(event);
        updateEvents(event.target, 'click');
        }, true );

    /* Set up a key press event listener on the window. */
    window.addEventListener('keypress', function (event) {
        console.log(event);
        updateEvents(event.target, 'keypress', event.key);
    });

    window.hasAddedEventListener = true;

    /**
     * Returns an XPath expression that can be used to select the given HTML element in an XML document.
     * @param {HTMLElement} element - The HTML element.
     * @returns {string} - The XPath expression.
     */
    function getXPath(element) {
        /* Start with the element's tag name (in lower case). */
        let xpath = `/${element.tagName.toLowerCase()}`;
        /* If the element has an id attribute, include the id attribute to uniquely identify the element. */
        if (element.id) {
            xpath += `[@id="${element.id}"]`;
        }
        /* If the element does not have an id attribute, determine the element's position among its siblings with the same tag name. */
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
        /* Repeat this process for each of the element's ancestors, until we reach the HTML element at the root of the document. */
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
        xpath = `/` + xpath;
        return xpath
    }

    /**
     * Called by the event listeners. This will send the recorded action to the local server.
     * @param element The element which the user interacted with.
     * @param type What the user did. Ex: Click, Type(key press)
     * @param key If the user typed something, this will contain what was typed.
     */
    function updateEvents(element, type, key = '') {
        var xpath = getXPath(element);
        
        fetch("http://localhost:8000/", {
            method: "POST",
            body: JSON.stringify({
                site: window.location.origin,
                action_type: type,
                xpath: xpath,
                value: key
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            console.log(response.status);

            return response.json();
        })
        .catch(error => {
            console.error(error);
        });

    }
})();


// function updateEvents(element, type, key = '') {
//     var data = JSON.parse(localStorage.myEvents || '[]');

//     var xpath = getXPath(element);
//     if (type == 'keypress' && data.length && data[data.length - 1].type === "keypress")
//         data[data.length - 1].value += key;
//     else {
//         data.push({
//             type: type,
//             xpath: xpath,
//             value: key
//         });
//     }

//     localStorage.myEvents = JSON.stringify(data);
// }