var currentPage = 0; // current page is initially 0

function showPage(pageNumber) {
    // display page number (starting at 0)

    if (pageNumber > 2) {
        pageNumber = 2;
    }
    else if (pageNumber < 0) {
        pageNumber = 0;
    }

    var pages = document.getElementsByClassName("page");
    pages[currentPage].style.display = "none";
    pages[pageNumber].style.display = "block";
    window.scrollTo({
        top: 0,
        bottom: 0,
        behavior: "smooth"
    });

    currentPage = pageNumber;

    // fix prev/next buttons
    var prevButtons = document.getElementsByClassName("prevBtn");
    var nextButtons = document.getElementsByClassName("nextBtn");

    if (pageNumber == 0) {
        for (let i = 0; i < prevButtons.length; i++) {
            prevButtons[i].style.visibility = "hidden";
            prevButtons[i].style.cursor = "default";
        }
    }
    else {
        for (let i = 0; i < prevButtons.length; i++) {
            prevButtons[i].style.visibility = "visible";
            prevButtons[i].style.cursor = "pointer";
        }
    }
    
    // change next to submit
    if (pageNumber == (pages.length - 1)) {
        for (let i = 0; i < nextButtons.length; i++) {
            nextButtons[i].innerHTML = "Download";
            nextButtons[i].title = "Download Word Document";
        }
    }
    else {
        for (let i = 0; i < nextButtons.length; i++) {
            nextButtons[i].innerHTML = "Next";
            nextButtons[i].title = "Next Page";
        }
    }

    // display page indicator
    fixStepIndicator(pageNumber)
}

function nextPrev(n) {
    var pages = document.getElementsByClassName("page");

    // submits the form
    if (currentPage + n >= pages.length) {
        if (validateForm(false)) {
            document.body.style.cursor = "progress";
            document.getElementById("bulletin_form").submit();
            document.body.style.cursor = "default";
        }
        return false;
    }

    // display tab if not submitting
    showPage(currentPage + n);
}

function validateForm(clear) {
    // clear refers to whether or not to just remove invalid flags
    // function that displays unvalidated forms and prevents submission
    var pages = document.getElementsByClassName("page");
    var inputs;
    var pageToShow;
    var foundFirstInvalid = false;

    // check all pages
    for (let j = 0; j < pages.length; j++) {
        inputs = pages[j].querySelectorAll("input[type=date], input[type=text], input[type=checkbox], select, textarea");
        // check all inputs on each page
        for (let i = 0; i < inputs.length; i++) {
            if (!clear && inputs[i].hasAttribute("required")) { // if required input and not clearing
                if (inputs[i].value == "") { // and input empty
                    // add an "invalid" class to the field if it doesn't have it
                    if (!inputs[i].classList.contains("invalid")) {
                        inputs[i].classList.add("invalid");
                    }
                    if (!foundFirstInvalid) { // display the first invalid one page
                        pageToShow = j;
                        foundFirstInvalid = true;
                    }
                }
                else if (inputs[i].classList.contains("invalid")) { // remove invalid flag if validated
                    inputs[i].classList.remove("invalid");
                }
            }
            else if (clear && inputs[i].classList.contains("invalid")) {
                inputs[i].classList.remove("invalid");
            }
        }
    }

    if (foundFirstInvalid && !clear) { // display invalid and change page
        showPage(pageToShow);
        return false;
    }

    return true;
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var steps = document.getElementsByClassName("step");
    for (let i = 0; i < steps.length; i++) {
        steps[i].classList.remove("active");
    }

    steps[n].classList.add("active");
    steps[n+3].classList.add("active"); // where 3 is the number of pages
}

window.addEventListener("load", 
    function() {
        showPage(currentPage);
    }
)