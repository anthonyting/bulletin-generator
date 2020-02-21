var dragSrcEl = null;

function colDragStart(b) {
    this.style.opacity = "0.4";
    if (this.className == "date1") {
        var a = true;
    } else {
        var a = false;
    }
    dragSrcEl = this;
    date1Nodes = document.querySelectorAll("td.col-0");
    date2Nodes = document.querySelectorAll("td.col-1");
    dragValues = [];
    for (let i = 0; i < date1Nodes.length; i++) {
        dragValues.push([date1Nodes[i].querySelector("input").value, date2Nodes[i].querySelector("input").value]);
        if (a) {
            date1Nodes[i].style.opacity = "0.4";
        } else {
            date2Nodes[i].style.opacity = "0.4";
        }
    }
    b.dataTransfer.effectAllowed = "move"
}

function colDragOver(a) {
    if (a.preventDefault) {
        a.preventDefault()
    }
    a.dataTransfer.dropEffect = "move";
    this.classList.add("over");
    if (dragSrcEl != this) {
        for (let i = 0; i < date1Nodes.length; i++) {
            date1Nodes[i].querySelector("input").value = dragValues[i][1];
            date2Nodes[i].querySelector("input").value = dragValues[i][0]
        }
    }
    return false;
}

function colDragLeave(a) {
    this.classList.remove("over");
    for (let i = 0; i < date1Nodes.length; i++) {
        date1Nodes[i].querySelector("input").value = dragValues[i][0];
        date2Nodes[i].querySelector("input").value = dragValues[i][1]
    }
}

function colDrop(a) {
    this.classList.remove("over");
    if (a.stopPropagation) {
        a.stopPropagation()
    }
    return false;
}

function colDragEnd(a) {
    this.style.opacity = "1";
    for (let i = 0; i < date1Nodes.length; i++) {
        date1Nodes[i].style.opacity = "1";
        date2Nodes[i].style.opacity = "1"
    } [].forEach.call(titles, function (b) {
        b.classList.remove("over")
    })
}
window.addEventListener("load", function () {
    titles = [].slice.call(document.querySelectorAll("table tr.title th"), 1, 3); // ignore first empty title
    [].forEach.call(titles, function (a) {
        a.addEventListener("dragstart", colDragStart, false);
        a.addEventListener("dragover", colDragOver, false);
        a.addEventListener("dragleave", colDragLeave, false);
        a.addEventListener("drop", colDrop, false);
        a.addEventListener("dragend", colDragEnd, false)
    })
});