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
javascript: (function () {
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