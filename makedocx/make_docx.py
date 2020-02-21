import docx as d
import json
import string
import os
import typing

from . import inputs
import makedocx.pages.page_one as make_page_one
import makedocx.pages.page_two as make_page_two
import makedocx.pages.front_page as make_front_page
import makedocx.pages.back_page as make_back_page

def getFilename(I: inputs) -> str:
    if I.choir:
        if I.communion:
            return "choir+communion.docx"
        return "choir.docx"
    if I.communion:
        return "communion.docx"
    return "base.docx"

def makeDocx(directory: str, I: inputs.Inputs) -> str:
    """
    Returns name of file created in the directory provided.
    """

    # creates an absolute path for this file
    templateLocation = os.path.join(os.path.dirname(__file__), './templates')

    if not os.path.isdir(templateLocation):
        raise OSError("Template Directory not found.")

    document = d.Document(f"{templateLocation}/{getFilename(I)}")

    make_front_page.makePage(document, I)
    make_page_one.makePage(document, I)
    make_page_two.makePage(document, I)
    make_back_page.makePage(document, I)

    filename = f"{I.month}-{I.day}-{I.year}.docx"

    document.save(f"{directory}/{filename}")
    return filename