from database import Database
from bson.objectid import ObjectId
import argparse


class Editer:
    def __init__(self):
        self.database = Database()
        self.database.connect()

    def read_all(self):
        urls = self.database.urls.find({})
        for url in urls:
            print(url)

    def get_document(self, object_id):
        url_id = {"_id": ObjectId(object_id)}
        url = self.database.urls.find_one(url_id)
        rep = f"{url['_id']} {url['alias']} -> {url['url']}: {url['time']}"
        return {"url": url, "rep": rep, "_id": url_id}

    def edit(self, object_id):
        doc = self.get_document(object_id)
        print(doc['rep'])
        edit = input("Change alias or url: [a/u]: ")
        if edit.upper() == "A":
            new_alias = input("New alias: ")
            self.database.urls.find_one_and_update(
                    doc['_id'],
                    {"$set": {"alias": new_alias}}
            )
            print(new_alias)
        elif edit.upper() == "U":
            new_url = input("New url: ")
            new_url = self.database.valid_url(new_url)
            self.database.urls.find_one_and_update(
                doc['_id'],
                {"$set": {"url": new_url}}
            )
            print(new_url)

    def delete_document(self, object_id):
        doc = self.get_document(object_id)
        delete = input(f"{doc['rep']}\nDelete the document [Y/n]: ")
        if delete.upper() == "Y":
            print(self.database.urls.delete_one(doc['_id']))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", help="Edit with object id")
    parser.add_argument("-d", help="Delete delete document by id")
    parser.add_argument("-a", help="All", action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    editer = Editer()
    command = parse()
    if command.e is not None:
        editer.edit(command.e)
    if command.d is not None:
        editer.delete_document(command.d)
    if command.a:
        editer.read_all()
