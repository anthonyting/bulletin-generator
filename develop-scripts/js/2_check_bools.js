// if checkboxes are not checked, files are not required

function choirBool() {
    var b = document.getElementById("choirF");
    var a = document.getElementById("choirTextC");
    if (document.getElementById("choirBool").checked) {
        a.setAttribute("required", "");
        b.style.display = "block"
    } else {
        a.removeAttribute("required");
        b.style.display = "none"
    }
}

function holy_communionBool() {
    var a = document.getElementById("holy_communionF");
    var b = document.getElementById("holy_communionTextC");
    if (document.getElementById("holy_communionBool").checked) {
        b.setAttribute("required", "");
        a.style.display = "block"
    } else {
        b.removeAttribute("required");
        a.style.display = "none"
    }
}

function checkBoth() {
    choirBool();
    holy_communionBool()
}
window.addEventListener("load", function () {
    checkBoth()
});