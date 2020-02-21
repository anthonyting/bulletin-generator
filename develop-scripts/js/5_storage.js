function getInputs() {
    var page_one = page_one_inputs();
    var page_two = page_two_inputs();
    var page_three = page_three_inputs();
    var all = {"page_one": page_one, "page_two": page_two, "page_three": page_three};
    all.version = "1.0";
    localStorage.setItem("all", JSON.stringify(all));
}

function fillInputs() {
    if (!localStorage.getItem("all")) {
        // implies first visit, so no local storage
        return;
    }
    var all = JSON.parse(localStorage.getItem("all"));

    if (Array.isArray(all)) { // legacy storage adapter
        var a = document.querySelectorAll("input[type=date], input[type=text], input[type=checkbox], select, textarea");
        for (let i = 0; i < a.length; i++) {
            if (typeof (all[i]) === "boolean") {
                a[i].checked = all[i];
            } else {
                a[i].value = all[i];
            }
        }
        console.warn("Legacy storage loaded.");
    }
    else {
        var page_one = all.page_one;
        var page_two = all.page_two;
        var page_three = all.page_three;

        // page one
        document.getElementById("date").value = page_one.date;
        document.getElementById("front_title").value = page_one.front_title;
        document.getElementById("order_of_worship_title").value = page_one.order_of_worship_title;
        document.getElementById("choirBool").checked = page_one.choirBool;
        document.getElementById("holy_communionBool").checked = page_one.holy_communionBool;
        document.getElementById("call_to_worshipC").value = page_one.call_to_worshipC;
        document.getElementById("call_to_worshipE").value = page_one.call_to_worshipE;
        document.getElementById("hymnC").value = page_one.hymnC;
        document.getElementById("hymnE").value = page_one.hymnE;
        document.getElementById("responsive_readingC").value = page_one.responsive_readingC;
        document.getElementById("responsive_readingE").value = page_one.responsive_readingE;
        document.getElementById("choirTextC").value = page_one.choirTextC;
        document.getElementById("choirTextE").value = page_one.choirTextE;
        document.getElementById("scripture_readingC").value = page_one.scripture_readingC;
        document.getElementById("scripture_readingE").value = page_one.scripture_readingE;
        document.getElementById("sermonC").value = page_one.sermonC;
        document.getElementById("sermonE").value = page_one.sermonE;
        document.getElementById("responding_hymnC").value = page_one.responding_hymnC;
        document.getElementById("responding_hymnE").value = page_one.responding_hymnE;
        document.getElementById("holy_communionTextC").value = page_one.holy_communionTextC;
        document.getElementById("holy_communionTextE").value = page_one.holy_communionTextE;

        // page two
        for (let i = 0; i < 12; i++) {
            document.getElementById("announcements-" + i.toString() + "-bold").value = page_two.announcements[i][0];
            document.getElementById("announcements-" + i.toString() + "-text").value = page_two.announcements[i][1];
        }

        // page three
        for (let i = 0; i < 4; i++) {
            document.getElementById("prayers-" + i.toString()).value = page_three.prayers[i];
        }
        
        for (let i = 0; i < 6; i++) {
            document.getElementById("schedules-" + i.toString() + "-week1").value = page_three.schedules[i][0];
            document.getElementById("schedules-" + i.toString() + "-week2").value = page_three.schedules[i][1];
        }

        document.getElementById("book").value = page_three.book;
        document.getElementById("chapter").value = page_three.chapter;
        document.getElementById("verses").value = page_three.verses;
        document.getElementById("box").value = page_three.box;
    }
}

function clearPageInputs(pageId, message) {
    if (!message || confirm(message)) { // if there is no message or the message is confirmed
        var queryString = "input[type=file], #" + pageId + " input[type=date], #" + pageId + " input[type=text], #"+ pageId +  
                         " input[type=checkbox], #" + pageId + " select, #" + pageId + " textarea";
        var a = document.querySelectorAll(queryString);
        for (let i = 0; i < a.length; i++) {
            if (a[i].type == "checkbox") {
                a[i].checked = false;
            } else {
                if (a[i].type == "file") {
                    a[i].value = null;
                } else {
                    a[i].value = "";
                }
            }
        }
        validateForm(true); // clear invalid tags defined in change_pages.js
        return true;
    } else {
        return false;
    }
}

function clearInputs(message) {
    if (clearPageInputs("page0", message) && clearPageInputs("page1", null) && clearPageInputs("page2", null)) {
        return true;
    } else {
        return false;
    }
}

function page_one_inputs() {
    var page_one = {};
    page_one.date = document.getElementById("date").value;
    page_one.front_title = document.getElementById("front_title").value;
    page_one.order_of_worship_title = document.getElementById("order_of_worship_title").value;
    page_one.choirBool = document.getElementById("choirBool").checked;
    page_one.holy_communionBool = document.getElementById("holy_communionBool").checked;
    page_one.call_to_worshipC = document.getElementById("call_to_worshipC").value;
    page_one.call_to_worshipE = document.getElementById("call_to_worshipE").value;
    page_one.hymnC = document.getElementById("hymnC").value;
    page_one.hymnE = document.getElementById("hymnE").value;
    page_one.responsive_readingC = document.getElementById("responsive_readingC").value;
    page_one.responsive_readingE = document.getElementById("responsive_readingE").value;
    page_one.choirTextC = document.getElementById("choirTextC").value;
    page_one.choirTextE = document.getElementById("choirTextE").value;
    page_one.scripture_readingC = document.getElementById("scripture_readingC").value;
    page_one.scripture_readingE = document.getElementById("scripture_readingE").value;
    page_one.sermonC = document.getElementById("sermonC").value;
    page_one.sermonE = document.getElementById("sermonE").value;
    page_one.responding_hymnC = document.getElementById("responding_hymnC").value;
    page_one.responding_hymnE = document.getElementById("responding_hymnE").value;
    page_one.holy_communionTextC = document.getElementById("holy_communionTextC").value;
    page_one.holy_communionTextE = document.getElementById("holy_communionTextE").value;
    return page_one;
}

function page_two_inputs() {
    var page_two = {};
    page_two.announcements = [["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""],["",""]]; // 12 announcements
    for (let i = 0; i < 12; i++) {
        page_two.announcements[i][0] = document.getElementById("announcements-" + i.toString() + "-bold").value;
        page_two.announcements[i][1] = document.getElementById("announcements-" + i.toString() + "-text").value;
    }
    return page_two;
}

function page_three_inputs() {
    var page_three = {};
    page_three.prayers = [];
    for (let i = 0; i < 4; i++) {
        page_three.prayers[i] = document.getElementById("prayers-" + i.toString()).value;
    }

    page_three.schedules = [["",""],["",""],["",""],["",""],["",""],["",""]]; // 6 dates
    for (let i = 0; i < 6; i++) {
        page_three.schedules[i][0] = document.getElementById("schedules-" + i.toString() + "-week1").value;
        page_three.schedules[i][1] = document.getElementById("schedules-" + i.toString() + "-week2").value;
    }

    page_three.book = document.getElementById("book").value;
    page_three.chapter = document.getElementById("chapter").value;
    page_three.verses = document.getElementById("verses").value;
    page_three.box = document.getElementById("box").value;
    return page_three;
}

function makeInputListeners() {
    var inputs = document.querySelectorAll("input[type=file], input[type=date], input[type=text], input[type=checkbox], select, textarea");
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener("change", function() {
            getInputs();
            document.title = "Bulletin - Saving.";
            setTimeout(function() {
                document.title = "Bulletin - Saving..";
                setTimeout(function() {
                    document.title = "Bulletin - Saving...";
                    setTimeout(function() {
                        document.title = "Bulletin";
                    }, 550);
                }, 300);
            }, 300);
        });
    }
}

window.addEventListener("beforeunload", function () {
    getInputs();
});
window.addEventListener("load", function () {
    fillInputs();
    makeInputListeners();
});