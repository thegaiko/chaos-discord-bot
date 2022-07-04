from datetime import date, datetime
from email import message
from unittest import result
from pymongo import MongoClient
import datetime

client = MongoClient(
    'mongodb+srv://gewwworg:Qscqsc.02@cluster0.jn5m4.mongodb.net/?retryWrites=true&w=majority')

mydb = client["chaos"]
mycol = mydb["chaos_members"]

def getUser():
    result = []
    for x in mycol.find({}, {"_id":0}): 
        result.append(x['id'])
    return(result)

def addAva(user):
    mycol.update_one({'id': user['id']},{ "$set":  {'avatar': user['avatar']}})
    return True

def createUser(model):
    mycol.insert_one(model)

def delReq(id):
    mycol = mydb["requests"]
    myquery = { "id": id}
    mycol.delete_one(myquery)

def verifyDb(name, id, start_date, end_date, avatar, token):
    mycol = mydb["chaos_members"]
    mycol.update_one({'token': token},{ "$set":  {'name': name, 'id': id, 'avatar': avatar, 'start_date': start_date, 'end_date': end_date}})
    

def takeName(id):
    name = mycol.find_one({"id": id})["name"]
    return name

def subscribe(id):
    time1 = mycol.find_one({'id': id})["end_date"]
    delta = datetime.timedelta(days=30)
    time2 = time1 + delta
    mycol.update_one({'id': id},{ "$set":  {'end_date': time2}})
    return(mycol.find_one({'id': id})["end_date"])

def checkUser(id):
    user = mycol.find_one({"id": id})
    userModel = [user["name"], user["id"], user["token"], user["price"], user["start_date"], user["end_date"], user["retry"]]
    return userModel


def checkSub():
    kick_members = []
    for member in mycol.find(): 


        retry = member["retry"]
        end_date = member["end_date"]
        delta = datetime.timedelta(days=int(retry))
        end_date = end_date + delta

        end_date = end_date.day
        now = datetime.datetime.now().day
        if now >= end_date:
            kick_members.append(member["id"])
        else:
            pass
    return kick_members


def getRequestsList():
    mycol = mydb["requests"]
    res = []
    for x in mycol.find({}, {"_id":0}): 
            res.append({"id": x['id'], "name": x['name'], "discord": x['discord'], "email": x['email'], "about": x['about']})
    return res

def delMessages(res):
    mycol = mydb["passive_messages_eng"]
    myquery = { "message": res}
    mycol.delete_one(myquery)