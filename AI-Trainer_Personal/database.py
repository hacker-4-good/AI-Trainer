'''
Backend for AI-Trainer App:

create -> creation of new user on our app

update -> update the existing information of user

delete -> delete the mention user

read -> display the information of particular user
'''


import pymongo
import random

client = pymongo.MongoClient("mongodb://localhost:27017")

mydb = client["AI-Trainer"]

user = mydb["UserLoginData"]

id = int(random.random()*100)

def check_user(username):
    for i in mydb.user.find({}):
        if i["Username"]==username:
            return True
    return False

def check_pass(password):
    for i in mydb.user.find({}):
        if i["Password"]==password:
            return True
    return False


def create(id, username, email, password):
    if check_user(username):
        pass
    elif username!= "":
        mydb.user.insert_one({"id":id, "Username":username, "Email":email, "Password":password})


def add_info(id, age, weight, height):
    mydb.user.update_one({"id":id}, {"$set":{"Age":age, "Weight":weight, "Height":height}})


def update(prev_username, username, email, password):
    mydb.user.update({"Username":prev_username}, {"Username":username, "Email":email, "Password":password})


def delete(username):
    mydb.user.delete_one({"Username":username})


def read(username):
    for i in mydb.user.find({"Username":username}):
        print(i["Username"])




