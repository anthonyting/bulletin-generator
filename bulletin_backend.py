from flask import Flask, render_template, redirect, url_for, flash

import makedocx.inputs as inputs
import makedocx.make_docx as make_docx
from makedocx.pages.docx_exceptions import *

import typing
from datetime import datetime
import json
import os

import forms.page_one
import forms.page_two
import forms.back_page
import forms.download

from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename

import traceback

csrf = CSRFProtect()

app = Flask(__name__)

csrf.init_app(app)
app.config["WTF_CSRF_TIME_LIMIT"] = None # until end of session

app.secret_key = os.environ.get("csrf_key")
app.config['OUTPUT_FOLDER'] = "./output"
app.config["DAILY_LIMIT"] = 500
app.config["LIMIT_POSITION"] = 0
app.config["DATE"] = datetime.today().date()

app.jinja_env.filters['zip'] = zip # allow the zip function in template

@app.route(f"/output/<filetype>/<filename>",methods=['GET','POST']) # served with nginx
def download_file(filetype, filename):
    flash("File Downloaded", "success") # nginx handles sending the file

def deleteOldestFile(directory: str, filetype: str):
    files = os.listdir(f"{directory}")
    full_path = [f"{directory}/{file}" for file in files]

    filesToDelete = [file for file in full_path if file.endswith(f".{filetype}")] # checking file extensions

    for _ in range(5, len(filesToDelete)):
        oldestFile = min(filesToDelete, key=os.path.getctime)
        os.remove(oldestFile)
        filesToDelete.remove(oldestFile)

@app.route('/', methods=['GET','POST'])
def bulletin():
    I = inputs.Inputs()

    pageOne = forms.page_one.pageOne() # creates all forms for page one
    pageOneValidation = pageOne["validation"]

    pageTwo = forms.page_two.pageTwo()

    backPage = forms.back_page.backPage()
    backPageValidation = backPage["validation"]

    downloadForm = forms.download.DownloadJson()

    if (downloadForm.download.data):
        try:
            assignPageOneInputs(I, pageOne)
            assignPageTwoInputs(I, pageTwo)
            assignBackPageInputs(I, backPage)
            if (I.date):
                filename = f"{datetime.strftime(I.date, '%m-%d-%Y')}.json"
            else:
                filename = "0-0-0.json"
            I.toJson(f"{app.config['OUTPUT_FOLDER']}/json", filename)
            deleteOldestFile(f"{app.config['OUTPUT_FOLDER']}/json", "json")
            return redirect(url_for('download_file', filetype="json",filename=filename,dl=1))
        except Exception as e:
            flash(f"Error Saving File: {e}", "error")
            print(f"{type(e)}, {e}")
            return redirect(url_for("bulletin"))
    
    choirValidation, holy_communionValidation = boolValidation(pageOne, pageOne["boolForms"].choirBool.data, pageOne["boolForms"].holy_communionBool.data)

    # validate forms
    if (pageOneValidation and backPageValidation and choirValidation and holy_communionValidation):

        assignPageOneInputs(I, pageOne)
        assignPageTwoInputs(I, pageTwo)
        assignBackPageInputs(I, backPage)

        # limit requests to "DAILY_LIMIT" config
        if (app.config["DATE"] != datetime.today().date()):
            app.config["LIMIT_POSITION"] = 0
            app.config["DATE"] = datetime.today().date()
        else:
            app.config["LIMIT_POSITION"] += 1

        if (app.config["LIMIT_POSITION"] > app.config["DAILY_LIMIT"]):
            flash("Error: Too many requests today. Try again tommorow", "error")
            return redirect(url_for("bulletin"))

        flash("Success: Download File.", "success")

        # create file based on inputs
        try:
            filename = make_docx.makeDocx(f"{app.config['OUTPUT_FOLDER']}/docx", I)
            deleteOldestFile(f"{app.config['OUTPUT_FOLDER']}/docx", "docx")
        except VerseNotFound as e:
            flash(f"Scripture verse not found: {e}", "error")
            return redirect(url_for("bulletin"))
        except Exception as e:
            flash(f"Error Making Document: {e}", "error")
            print(f"{type(e)}, {e}", flush=True)
            return redirect(url_for("bulletin"))

        return redirect(url_for('download_file',filetype="docx",filename=filename,dl=1))
    
    return render_template('bulletin.html', downloadForm=downloadForm, pageOne=pageOne, pageTwo=pageTwo.announcements, backPage=backPage)

def assignPageOneInputs(I: inputs.Inputs, pageOne: dict):
    OWForms = pageOne["order_of_worship"]

    # adds date
    if (pageOne["date"].date.data):
        I.year = pageOne["date"].date.data.year
        I.month = pageOne["date"].date.data.month
        I.day = pageOne["date"].date.data.day

    # adds front title
    if (pageOne["front_title"].front_title.data):
        I.front_page_title = pageOne["front_title"].front_title.data

    # adds choir and communion
    I.choir = pageOne["boolForms"].choirBool.data
    I.communion = pageOne["boolForms"].holy_communionBool.data

    # adds order of worship title
    if (pageOne["order_of_worship_title"].order_of_worship_title.data):
        I.order_of_worship_title = pageOne["order_of_worship_title"].order_of_worship_title.data

    # adds order of worship, ignoring empty entries
    o = I.order_of_worship
    assignOW(o, "call_to_worship", OWForms)
    assignOW(o, "hymn", OWForms)
    assignOW(o, "responsive_reading", OWForms)
    assignOW(o, "choir", OWForms)
    assignOW(o, "scripture_reading", OWForms)
    assignOW(o, "sermon", OWForms)
    assignOW(o, "responding_hymn", OWForms)

def assignPageTwoInputs(I: inputs.Inputs, pageTwo):

    # assign announcements
    I.num_of_announcements = 0

    for announcement in pageTwo.announcements:
        if (announcement.bold.data):
            I.announcements[I.num_of_announcements]["bold"] = announcement.bold.data
            I.announcements[I.num_of_announcements]["text"] = announcement.text.data
            I.num_of_announcements += 1

    if (I.num_of_announcements < 1):
        I.num_of_announcements = 1
    elif (I.num_of_announcements > 12):
        I.num_of_announcements = 12

def assignBackPageInputs(I: inputs.Inputs, backPage):

    # assign prayers
    I.prayer_count = 0

    for prayer in backPage["prayers"].prayers:
        if (prayer.data != ""):
            I.prayers[I.prayer_count] = prayer.data
            I.prayer_count += 1
    
    if (I.prayer_count < 1):
        I.prayer_count = 1
    elif (I.prayer_count > 4):
        I.prayer_count = 4

    count = 0
    for job in backPage["schedules"].schedules:
        if (count > 5):
            break
        I.schedules[count][0] = job.week1.data
        I.schedules[count][1] = job.week2.data
        count += 1

    englishBooks = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Proverbs", "Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"]
    chineseBooks = ["創世記", "出埃及記", "利未記", "民數記", "申命記", "約書亞記", "士師記", "路得記", "撒母耳記上", "撒母耳記下", "列王紀上", "列王紀下", "歷代志上", "歷代志下", "以斯拉記", "尼希米記", "以斯帖記", "約伯記", "詩篇", "箴言", "傳道書", "雅歌", "以賽亞書", "耶利米書", "耶利米哀歌", "以西結書", "但以理書", "何西阿書", "約珥書", "阿摩司書", "俄巴底亞書", "約拿書", "彌迦書", "那鴻書", "哈巴谷書", "西番雅書", "哈該書", "撒迦利亞", "瑪拉基書", "馬太福音", "馬可福音", "路加福音", "約翰福音", "使徒行傳", "羅馬書", "歌林多前書", "歌林多後書", "加拉太書", "以弗所書", "腓立比書", "歌羅西書", "帖撒羅尼迦前書", "帖撒羅尼迦後書", "提摩太前書", "提摩太後書", "提多書", "腓利門書", "希伯來書", "雅各書", "彼得前書", "彼得後書", "約翰一書", "約翰二書", "約翰三書", "猶大書", "启示录"]

    if (backPage["scriptures"].book.data):
        I.scriptures["book_num"] = backPage["scriptures"].book.data
        I.scriptures["book_ch"] = chineseBooks[backPage["scriptures"].book.data]
        I.scriptures["book"] = englishBooks[backPage["scriptures"].book.data]
    I.scriptures["chapter"] = backPage["scriptures"].chapter.data
    I.scriptures["verses"] = str(backPage["scriptures"].verses.data) # possibly change scripture.verses into a regex checked stringfield for things like "1-5"

    I.last_box = backPage["last_box"].box.data

    return

def boolValidation(pageOne, inputChoir, inputCommunion):
    # if the checkbox isn't checked, don't validate the corresponding entry

    if (not inputChoir):
        choirValidation = True
    else:
        choirValidation = pageOne["choirValidation"]
    
    if (not inputCommunion):
        holy_communionValidation = True
    else:
        holy_communionValidation = pageOne["holy_communionValidation"]

    return choirValidation, holy_communionValidation

def assignOW(orderOfWorship: dict, section: str, OWForms: dict):
    """
    Assigns input object's order_of_worship depending on form inputs
    """

    # first in section is chinese
    # second in section is english

    form = iter(OWForms[section])
    chinese = next(form)
    english = next(form)

    if (chinese.data):
        orderOfWorship[section][0] = chinese.data
    
    if (english.data):
        orderOfWorship[section][1] = english.data