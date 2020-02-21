from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField, SelectField, TextAreaField
from wtforms.validators import InputRequired

class prayerF(FlaskForm):
    prayers = FieldList(StringField("",render_kw={"autocomplete": "off","onfocus":"removeDraggable()","onBlur":"addDraggable()"}),min_entries=4,max_entries=4)

class jobF(FlaskForm):
    week1 = StringField("",validators=[InputRequired()],render_kw={"autocomplete": "off","onfocus":"removeDraggable()","onBlur":"addDraggable()"})
    week2 = StringField("",validators=[InputRequired()],render_kw={"autocomplete": "off","onfocus":"removeDraggable()","onBlur":"addDraggable()"})

class schedulesF(FlaskForm):
    schedules = FieldList(FormField(jobF), min_entries=6, max_entries=6)

class scriptureF(FlaskForm):
    books = [
        (
            0,
            "Genesis 創世記"
        ),
        (
            1,
            "Exodus 出埃及記"
        ),
        (
            2,
            "Leviticus 利未記"
        ),
        (
            3,
            "Numbers 民數記"
        ),
        (
            4,
            "Deuteronomy 申命記"
        ),
        (
            5,
            "Joshua 約書亞記"
        ),
        (
            6,
            "Judges 士師記"
        ),
        (
            7,
            "Ruth 路得記"
        ),
        (
            8,
            "1 Samuel 撒母耳記上"
        ),
        (
            9,
            "2 Samuel 撒母耳記下"
        ),
        (
            10,
            "1 Kings 列王紀上"
        ),
        (
            11,
            "2 Kings 列王紀下"
        ),
        (
            12,
            "1 Chronicles 歷代志上"
        ),
        (
            13,
            "2 Chronicles 歷代志下"
        ),
        (
            14,
            "Ezra 以斯拉記"
        ),
        (
            15,
            "Nehemiah 尼希米記"
        ),
        (
            16,
            "Esther 以斯帖記"
        ),
        (
            17,
            "Job 約伯記"
        ),
        (
            18,
            "Psalm 詩篇"
        ),
        (
            19,
            "Proverbs 箴言"
        ),
        (
            20,
            "Ecclesiastes 傳道書"
        ),
        (
            21,
            "Song of Songs 雅歌"
        ),
        (
            22,
            "Isaiah 以賽亞書"
        ),
        (
            23,
            "Jeremiah 耶利米書"
        ),
        (
            24,
            "Lamentations 耶利米哀歌"
        ),
        (
            25,
            "Ezekiel 以西結書"
        ),
        (
            26,
            "Daniel 但以理書"
        ),
        (
            27,
            "Hosea 何西阿書"
        ),
        (
            28,
            "Joel 約珥書"
        ),
        (
            29,
            "Amos 阿摩司書"
        ),
        (
            30,
            "Obadiah 俄巴底亞書"
        ),
        (
            31,
            "Jonah 約拿書"
        ),
        (
            32,
            "Micah 彌迦書"
        ),
        (
            33,
            "Nahum 那鴻書"
        ),
        (
            34,
            "Habakkuk 哈巴谷書"
        ),
        (
            35,
            "Zephaniah 西番雅書"
        ),
        (
            36,
            "Haggai 哈該書"
        ),
        (
            37,
            "Zechariah 撒迦利亞"
        ),
        (
            38,
            "Malachi 瑪拉基書"
        ),
        (
            39,
            "Matthew 馬太福音"
        ),
        (
            40,
            "Mark 馬可福音"
        ),
        (
            41,
            "Luke 路加福音"
        ),
        (
            42,
            "John 約翰福音"
        ),
        (
            43,
            "Acts 使徒行傳"
        ),
        (
            44,
            "Romans 羅馬書"
        ),
        (
            45,
            "1 Corinthians 歌林多前書"
        ),
        (
            46,
            "2 Corinthians 歌林多後書"
        ),
        (
            47,
            "Galatians 加拉太書"
        ),
        (
            48,
            "Ephesians 以弗所書"
        ),
        (
            49,
            "Philippians 腓立比書"
        ),
        (
            50,
            "Colossians 歌羅西書"
        ),
        (
            51,
            "1 Thessalonians 帖撒羅尼迦前書"
        ),
        (
            52,
            "2 Thessalonians 帖撒羅尼迦後書"
        ),
        (
            53,
            "1 Timothy 提摩太前書"
        ),
        (
            54,
            "2 Timothy 提摩太後書"
        ),
        (
            55,
            "Titus 提多書"
        ),
        (
            56,
            "Philemon 腓利門書"
        ),
        (
            57,
            "Hebrews 希伯來書"
        ),
        (
            58,
            "James 雅各書"
        ),
        (
            59,
            "1 Peter 彼得前書"
        ),
        (
            60,
            "2 Peter 彼得後書"
        ),
        (
            61,
            "1 John 約翰一書"
        ),
        (
            62,
            "2 John 約翰二書"
        ),
        (
            63,
            "3 John 約翰三書"
        ),
        (
            64,
            "Jude 猶大書"
        ),
        (
            65,
            "Revelation 启示录"
        )
    ] # this list was generated with a script

    book = SelectField("Book",coerce=int,choices=books,validators=[InputRequired()])
    chapter = IntegerField("Chapter",validators=[InputRequired()],render_kw={"autocomplete": "off"})
    verses = IntegerField("Verses",validators=[InputRequired()],render_kw={"autocomplete": "off"})

class lastBoxF(FlaskForm):
    box = TextAreaField("",validators=[InputRequired()],render_kw={"maxlength": "152"})

def backPage():
    prayers = prayerF()
    schedules = schedulesF()
    scriptures = scriptureF()
    last_box = lastBoxF()

    validation = prayers.validate_on_submit() and schedules.validate_on_submit() and scriptures.validate_on_submit() and last_box.validate_on_submit()

    return {
        "last_box": last_box,
        "prayers": prayers,
        "schedules": schedules,
        "scriptures": scriptures,
        "validation": validation,
        "jobs": [
            "講員",
            "主領",
            "領歌",
            "司琴",
            "招待, 奉献",
            "茶點"
        ]
    }