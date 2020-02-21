function updateDate() {
    var c = document.getElementById("date").value;
    if (!c) {
        return;
    }
    var b = new Date(c);
    var d = new Date(b.getTime() + 604800 * 1000);
    var a = b.getUTCMonth() + 1;
    var g = b.getUTCDate();
    var f = d.getUTCMonth() + 1;
    var e = d.getUTCDate();
    document.getElementsByClassName("date1")[0].innerHTML = a + "/" + g;
    document.getElementsByClassName("date2")[0].innerHTML = f + "/" + e
}
window.addEventListener("load", function () {
    document.getElementById("date").addEventListener("change", updateDate);
    updateDate()
});