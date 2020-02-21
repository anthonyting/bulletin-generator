from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FormField, FieldList

class announcementF(FlaskForm):
    bold = StringField("Bold: ",render_kw={"autocomplete": "off","placeholder":"Subject","onfocus":"removeDraggable()","onBlur":"addDraggable()"})
    text = TextAreaField("Text: ",render_kw={"autocomplete": "off","placeholder":"Text","onfocus":"removeDraggable()","onBlur":"addDraggable()"})

class announcements(FlaskForm):
    announcements = FieldList(FormField(announcementF),min_entries=12,max_entries=12)

def pageTwo():
    return announcements()