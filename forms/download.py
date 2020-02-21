from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired

class DownloadJson(FlaskForm):
    download = SubmitField("Save Inputs",render_kw={"formnovalidate": "true"}) # formnovalidate in html5 doesn't need a value, but here, render_kw does