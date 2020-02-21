var dragSrcEl = null;

function removeDraggable() {
    if (currentPage === 1) {
        active = document.activeElement.parentElement.parentElement;
    } else {
        active = document.activeElement.parentElement;
    }
    if (active.className == "row") {
        active.setAttribute("draggable", "false");
    }
}

function addDraggable() {
    if (active.className == "row") {
        active.setAttribute("draggable", "true");
    }
    active = null;
}

function createOriginals() {
    originalI = [];
    var rows;

    if (currentPage == 1) {
        rows = document.querySelectorAll("ol li.row");
        originalT = [];
    } else {
        rows = document.querySelectorAll("ul li.row");
    }
    for (let i = 0; i < rows.length; i++) {
        originalI.push(rows[i].getElementsByTagName("input")[0].value);
        if (currentPage == 1) {
            originalT.push(rows[i].getElementsByTagName("textarea")[0].value);
        }
    }
}

function handleDragStart(e) {
    this.style.opacity = "0.4";
    dragSrcEl = this;
    if (currentPage == 1) {
        dragValues = [this.getElementsByTagName("input")[0].value, this.getElementsByTagName("textarea")[0].value];
    } else {
        dragValues = [this.getElementsByTagName("input")[0].value];
    }
    e.dataTransfer.effectAllowed = "move";
    createOriginals();
}

function addRow(rowToAdd) {
    // moves rows by simulating a drag up from the last announcement (which must be empty)
    createOriginals();
    var rows;

    if (currentPage == 1) {
        rows = document.querySelectorAll("ol li.row");
    } else {
        rows = document.querySelectorAll("ul li.row");
    }

    var rowArr = Array.from(rows);
    var startingIndex = rowArr.indexOf(rowToAdd);

    if (rows[rows.length-1].getElementsByTagName("input")[0].value || (currentPage == 1 && rows[rows.length-1].getElementsByTagName("textarea")[0].value)) {
        // if the last announcement has some value, do not add a new row
        var listName;
        if (currentPage == 1) {
            listName = "Announcements";
        }
        else {
            listName = "Prayers";
        }
        alert(listName + " are full. Delete an entry to add another one.");
        return;
    }

    moveRows(rows.length-1, startingIndex, rows, ["", ""], rowToAdd);
    // make the new row empty
}

function deleteRow(rowToDelete) {
    // moves rows by simulating a drag down to the bottom,
    // but replacing the last row with empty

    if (!confirm("Are you sure you want to delete this row?")) {
        return;
    }

    createOriginals();

    var rows;
    if (currentPage == 1) {
        rows = document.querySelectorAll("ol li.row");
    } else {
        rows = document.querySelectorAll("ul li.row");
    }

    var rowArr = Array.from(rows);
    var startingIndex = rowArr.indexOf(rowToDelete);

    moveRows(startingIndex, rows.length-1, rows, ["", ""], rows[rows.length-1]);
    // make the final row empty
}

function moveRows(startingIndex, endingIndex, rows, valuesToReplace, replaceDestination) {
    // starting and ending Index are indices referring to the section to move
    // rows is an arraylike of li's
    // values is the source values in an array of max size 2

    var inputsToReplace = [];
    var textAreasToReplace = []; // only used for currentPage == 1
    if (startingIndex + 1 <= endingIndex) { // dragging down, elements go up
        for (let i = startingIndex + 1; i <= endingIndex; i++) { // create array to move
            inputsToReplace.push(originalI[i]);
            if (currentPage == 1) { // currentPage defined in change_pages.js
                textAreasToReplace.push(originalT[i]);
            }
        }
        for (let i = startingIndex, j = 0; i < endingIndex; i++, j++) { // fill values with created array
            rows[i].getElementsByTagName("input")[0].value = inputsToReplace[j];
            if (currentPage == 1) {
                rows[i].getElementsByTagName("textarea")[0].value = textAreasToReplace[j];
            }
        }
    } else { // dragging up, elements go down: uses similar logic with different indices
        for (let i = endingIndex; i < startingIndex; i++) {
            inputsToReplace.push(originalI[i]);
            if (currentPage == 1) {
                textAreasToReplace.push(originalT[i]);
            }
        }
        for (let i = endingIndex + 1, j = 0; i <= startingIndex; i++, j++) {
            rows[i].getElementsByTagName("input")[0].value = inputsToReplace[j];
            if (currentPage == 1) {
                rows[i].getElementsByTagName("textarea")[0].value = textAreasToReplace[j];
            }
        }
    }

    if (replaceDestination) {
        // put values to replace into the replace destination
        replaceDestination.getElementsByTagName("input")[0].value = valuesToReplace[0];
        if (currentPage == 1) {
            replaceDestination.getElementsByTagName("textarea")[0].value = valuesToReplace[1];
        }
    }
}

function handleDragOver(g) {
    // this refers to the thing being hovered over

    if (g.preventDefault) {
        g.preventDefault();
    }
    g.dataTransfer.dropEffect = "move";
    this.classList.add("over");
    if (dragSrcEl != this) {

        var rows;
        if (currentPage == 1) {
            rows = document.querySelectorAll("ol li.row");
        } else {
            rows = document.querySelectorAll("ul li.row");
        }
        
        var rowArr = Array.from(rows);
        var startingIndex = rowArr.indexOf(dragSrcEl);
        var endingIndex = rowArr.indexOf(this);
        moveRows(startingIndex, endingIndex, rows, dragValues, this);
        // move rows and swap the source values with the current over values
    }
    return false;
}

function handleDragLeave(b) {
    this.classList.remove("over");
    var rows;
    if (currentPage == 1) {
        rows = document.querySelectorAll("ol li.row");
    } else {
        rows = document.querySelectorAll("ul li.row");
    }
    for (let i = 0; i < rows.length; i++) {
        rows[i].getElementsByTagName("input")[0].value = originalI[i];
        if (currentPage == 1) {
            rows[i].getElementsByTagName("textarea")[0].value = originalT[i];
        }
    }
}

function handleDrop(a) {
    this.classList.remove("over");
    if (a.stopPropagation) {
        a.stopPropagation();
    }
    return false;
}

function handleDragEnd(a) {
    this.style.opacity = "1";
    [].forEach.call(rows, function (b) {
        b.classList.remove("over");
    });
}
window.addEventListener("load", function () {
    rows = document.getElementsByClassName("row");
    [].forEach.call(rows, function (a) {
        a.addEventListener("dragstart", handleDragStart, false);
        a.addEventListener("dragover", handleDragOver, false);
        a.addEventListener("dragleave", handleDragLeave, false);
        a.addEventListener("drop", handleDrop, false);
        a.addEventListener("dragend", handleDragEnd, false);
    });
});