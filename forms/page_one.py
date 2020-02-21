from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import DateField

class dateF(FlaskForm):
    date = DateField("Date (yyyy-mm-dd): ",format='%Y-%m-%d',validators=[InputRequired()])

class front_titleF(FlaskForm):
    front_title = StringField("Front Title",validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})

class order_of_worship_titleF(FlaskForm):
    order_of_worship_title = StringField("Order Of Worship Title",validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})

class boolF(FlaskForm):
    choirBool = BooleanField("詩班獻唱 Choir: ")
    holy_communionBool = BooleanField("敬設聖餐 Holy Communion: ")

class call_to_worshipF(FlaskForm):
    call_to_worshipC = StringField("宣召 Call To Worship: ", validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})
    call_to_worshipE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

class hymnF(FlaskForm):
    hymnC = StringField("唱詩 Hymn: ", validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})
    hymnE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

class responsive_readingF(FlaskForm):
    responsive_readingC = StringField("啟應經文 Responsive Reading: ", validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})
    responsive_readingE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

class choirTextF(FlaskForm):
    choirTextC = StringField("詩班獻唱 Choir: ",validators=[InputRequired()],render_kw={"placeholder": "中文"})
    choirTextE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

class scripture_readingF(FlaskForm):
    scripture_readingC = StringField("讀經 Scripture Reading: ", validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})
    scripture_readingE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

class sermonF(FlaskForm):
    sermonC = StringField("證道 Sermon: ", validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})
    sermonE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

class responding_hymnF(FlaskForm):
    responding_hymnC = StringField("回應詩 Responding Hymn: ", validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})
    responding_hymnE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

class holy_communionF(FlaskForm):
    holy_communionTextC = StringField("敬設聖餐 Holy Communion: ",validators=[InputRequired()],render_kw={"placeholder": "中文", "autocomplete": "off"})
    holy_communionTextE = StringField("",render_kw={"placeholder": "English", "autocomplete": "off"})

def pageOne():
    front_title = front_titleF()
    order_of_worship_title = order_of_worship_titleF()

    dateForms = dateF()
    boolForms = boolF()
    call_to_worship = call_to_worshipF()
    hymn = hymnF()
    responsive_reading = responsive_readingF()
    choirText = choirTextF()
    scripture_reading = scripture_readingF()
    sermon = sermonF()
    responding_hymn = responding_hymnF()
    holy_communion = holy_communionF()

    choirValidation = choirText.validate_on_submit()
    holy_communionValidation = holy_communion.validate_on_submit()

    validation = False
    if (front_title.validate_on_submit() and order_of_worship_title.validate_on_submit() and call_to_worship.validate_on_submit() and hymn.validate_on_submit()
    and responsive_reading.validate_on_submit() and scripture_reading.validate_on_submit() and sermon.validate_on_submit() and responding_hymn.validate_on_submit()
    and boolForms.validate_on_submit() and dateForms.validate_on_submit()):
        validation = True

    result =    {
                    "date": dateForms,
                    "front_title": front_title,
                    "boolForms": boolForms,
                    "order_of_worship_title": order_of_worship_title,
                    "order_of_worship": {
                        "call_to_worship": call_to_worship, 
                        "hymn": hymn,
                        "responsive_reading": responsive_reading,
                        "choir": choirText,
                        "scripture_reading": scripture_reading,
                        "sermon": sermon,
                        "responding_hymn": responding_hymn,
                        "holy_communion": holy_communion,
                    }, 
                    "validation": validation,
                    "choirValidation": choirValidation,
                    "holy_communionValidation": holy_communionValidation
                }

    return result