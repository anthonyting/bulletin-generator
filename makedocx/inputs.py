import typing
import json
from datetime import datetime

import os

class Inputs:
    def __init__(self, inputDict: dict=None):
        """
        Initialize Input object with a file, or a dictionary. If a file is provided, the dictionary is ignored.
        """
        if (inputDict):
            inputs = inputDict
        else:
            # creates an absolute path for this file
            with open(os.path.join(os.path.dirname(__file__), './templates/empty_input.json'),"r",encoding="utf8") as f:
                inputs: dict = json.load(f)

        # create pages
        front_page: dict = inputs["front_page"]
        page_one: dict = inputs["page_one"]
        page_two: dict = inputs["page_two"]
        back_page: dict = inputs["back_page"]

        # front page
        date: dict = front_page["date"]
        self.year: int = date["year"]
        self.month: int = date["month"]
        self.day: int = date["day"]
        self.front_page_title = front_page["title"]
        
        # page one
        self.order_of_worship_title: str = page_one["order_of_worship_title"]
        self.order_of_worship: dict = page_one["order_of_worship"]
        self.choir: bool = page_one["choir"]
        self.communion: bool = page_one["communion"]

        # page two
        self.announcements: list = page_two["announcements"]
        self.num_of_announcements: int = page_two["num_of_announcements"]
        if (self.num_of_announcements > 12): # max announcements will always be 12
            self.num_of_announcements = 12

        # back page
        self.prayers: list = back_page["prayers"]
        self.prayer_count: int = back_page["prayer_count"]
        self.schedules: list = back_page["schedules"]
        self.scriptures: dict = back_page["scriptures"]
        self.last_box: str = back_page["last_box"]

        # advanced settings for docx
        self._advanced = inputs["advanced"]
    
    @property
    def date(self):
        try:
            result = datetime.strptime(f"{self.month} {self.day} {self.year}", "%m %d %Y")
        except ValueError:
            result = None
        return result

    def toJson(self, directory: str, filename: str):
        # builds a dict object and saves a json file

        inputs = {}
        
        # front page
        front_page = {}
        inputs["front_page"] = front_page

        date = {}
        front_page["date"] = date
        date["year"] = self.year
        date["month"] = self.month
        date["day"] = self.day
        front_page["title"] = self.front_page_title

        # page one
        page_one = {}
        inputs["page_one"] = page_one
        page_one["order_of_worship_title"] = self.order_of_worship_title
        page_one["order_of_worship"] = self.order_of_worship
        page_one["choir"] = self.choir
        page_one["communion"] = self.communion

        # page two
        page_two = {}
        inputs["page_two"] = page_two
        page_two["announcements"] = self.announcements
        page_two["num_of_announcements"] = self.num_of_announcements
        if (self.num_of_announcements > 12): # max announcements will always be 12
            self.num_of_announcements = 12

        # back page
        back_page = {}
        inputs["back_page"] = back_page
        back_page["prayers"] = self.prayers
        back_page["prayer_count"] = self.prayer_count
        if (self.prayer_count > 4):
            self.prayer_count = 4
        back_page["schedules"] = self.schedules
        back_page["scriptures"] = self.scriptures
        back_page["last_box"] = self.last_box

        with open(f"{directory}/{filename}", "w+", encoding="utf8") as f:
            json.dump(inputs, f, ensure_ascii=False)