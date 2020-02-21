function handleFileSelect(e) {
    var file = e.target.files[0];
    var reader = new FileReader();
    reader.onload = (function (e) {
        return function (h) {
            try {
                var f = JSON.parse(h.target.result)
            } catch (err) {
                alert("Invalid File. Upload a properly formatted JSON file");
                console.log("Error: " + err);
                return
            }
            if (clearInputs("Are you sure you want to replace all inputs?")) {
                fill_page_one(f);
                fill_page_two(f.page_two);
                fill_page_three(f.back_page);
                validateForm(true); // in change_pages.js
            } else {
                document.querySelector("input[type=file]").value = null;
                return
            }
            checkBoth();
        }
    })(file);
    try {
        reader.readAsText(file);
    } catch (err) {}
}

function fill_page_one(c) {
    var d = c.page_one;
    var b = d.order_of_worship;
    var e = c.front_page["date"]["month"].toString();
    var a = c.front_page["date"]["day"].toString();
    if (e.length < 2) {
        e = "0" + e
    }
    if (a.length < 2) {
        a = "0" + a
    }
    document.getElementById("date").value = c.front_page["date"]["year"].toString() + "-" + e + "-" + a;
    document.getElementById("front_title").value = c.front_page["title"];
    document.getElementById("order_of_worship_title").value = d.order_of_worship_title;
    document.getElementById("choirBool").checked = d.choir;
    document.getElementById("holy_communionBool").checked = d.communion;
    document.getElementById("call_to_worshipC").value = b.call_to_worship[0];
    document.getElementById("call_to_worshipE").value = b.call_to_worship[1];
    document.getElementById("hymnC").value = b.hymn[0];
    document.getElementById("hymnE").value = b.hymn[1];
    document.getElementById("responsive_readingC").value = b.responsive_reading[0];
    document.getElementById("responsive_readingE").value = b.responsive_reading[1];
    document.getElementById("choirTextC").value = b.choir[0];
    document.getElementById("choirTextE").value = b.choir[1];
    document.getElementById("scripture_readingC").value = b.scripture_reading[0];
    document.getElementById("scripture_readingE").value = b.scripture_reading[1];
    document.getElementById("sermonC").value = b.sermon[0];
    document.getElementById("sermonE").value = b.sermon[1];
    document.getElementById("responding_hymnC").value = b.responding_hymn[0];
    document.getElementById("responding_hymnE").value = b.responding_hymn[1];
    document.getElementById("holy_communionTextC").value = b.holy_communion[0];
    document.getElementById("holy_communionTextE").value = b.holy_communion[1]
}

function fill_page_two(a) {
    for (let i = 0; i < a.num_of_announcements; i++) {
        document.getElementById("announcements-" + i.toString() + "-bold").value = a.announcements[i]["bold"];
        document.getElementById("announcements-" + i.toString() + "-text").value = a.announcements[i]["text"]
    }
}

function fill_page_three(a) {
    updateDate();
    for (let i = 0; i < a.prayer_count; i++) {
        document.getElementById("prayers-" + i.toString()).value = a.prayers[i]
    }
    for (let i = 0; i < a.schedules.length; i++) {
        document.getElementById("schedules-" + i.toString() + "-week1").value = a.schedules[i][0];
        document.getElementById("schedules-" + i.toString() + "-week2").value = a.schedules[i][1]
    }
    document.getElementById("book").value = a.scriptures["book_num"];
    document.getElementById("chapter").value = a.scriptures["chapter"];
    document.getElementById("verses").value = a.scriptures["verses"];
    document.getElementById("box").value = a.last_box
}
window.addEventListener("load", function () {
    document.getElementById("file").addEventListener("change", handleFileSelect, false)
});