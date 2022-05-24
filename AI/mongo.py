from datetime import date, datetime
from pymongo import MongoClient
import datetime

client = MongoClient(
    'mongodb+srv://gewwworg:Qscqsc.02@cluster0.jn5m4.mongodb.net/?retryWrites=true&w=majority')

mydb = client["chaos"]
mycol = mydb["chaos_members"]


def checkTOKEN(ACCESS_TOKEN):
    try:
        mycol.find_one({"token": ACCESS_TOKEN})["token"]
        return True
    except TypeError:
        return False