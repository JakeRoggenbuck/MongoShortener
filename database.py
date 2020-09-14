from pymongo import MongoClient
from dataclasses import dataclass
from datetime import datetime


def valid_url(url: str):
    """Check if the url is actually a correct url"""
    if url == "":
        return False
    if 'http' not in url:
        url = 'https://' + url
    return url


@dataclass
class Link:
    """Data class for making url entries"""
    alias: str
    url: str
    clicks: int

    def get_link_dict(self):
        """Return a dictionary with all the data

        Return the data in a dictionary with timestamp"""
        data = {
            "alias": self.alias,
            "url": self.url,
            "clicks": self.clicks,
            "time": datetime.now()
        }
        return data


class Database:
    def __init__(self, location="localhost", ip="127.0.0.1"):
        """Sets defaults for parameters"""
        self.location = location
        self.ip = ip

    def connect(self):
        """Make the client, connect the db and create the collections"""
        self.client = MongoClient()
        self.db = self.client.url_short
        self.urls = self.db.urls

    def check_alias(self, alias: str):
        """Return True if the alias exists, else return False"""
        result = self.urls.find_one({"alias": alias})
        # If exists return True
        if result is None:
            return False
        else:
            return True

    def get_url(self, alias: str):
        """Make qwery for alias, if it exists, increment clicks by one"""
        qwery = {"alias": alias}
        result = self.urls.find_one_and_update(qwery, {"$inc": {"clicks": 1}})
        # Return the url if it exists and return False if not
        if result is not None:
            return result['url']
        else:
            return False

    def add_alias(self, alias: str, url: str):
        """Add alias if it does not exist"""
        # Check if string is empty
        if alias == "":
            return False
        # Check if alias exists
        if not self.check_alias(alias):
            # Check if url is valid and complete
            if (url := valid_url(url)) is not False:
                # Make link object and get the dictionary of it
                link = Link(alias, url, 0).get_link_dict()
                # Insert the url object
                self.urls.insert_one(link)
                return True
        else:
            # Return False for an issue
            return False
