from pymongo import MongoClient
from pydantic import BaseModel
from collections.abc import Iterable

def connect():
    client = MongoClient(r"mongodb+srv://theunbestdaniel:<PASSWORD>@cluster0.xsfhv3a.mongodb.net/hell_oworld")

    db = client["hell_oworld"]
    collection = db["hell_oworld"]
    
    return collection

def add_one_document(doc):
    if doc.__bases__ == BaseModel:
        doc = doc.model_dump()
    collection = connect()
    collection.insert_one(doc)

def add_many_document(doc):
    if doc.__bases__ == BaseModel:
        doc = doc.model_dump()["data"]
    collection = connect()
    collection.insert_many(doc)

class query():
    @staticmethod
    def query(statement):
        collection = connect()
        return collection.find(statement)
    
    @staticmethod
    def user_data(user):
        if isinstance(user, Iterable):
            statement = {"user":{"$in":list(user)}}
        else:
            assert isinstance(user,int), "Type Error Bitch"
            statement = {"user":user}
        
        return query.query(statement)

    @staticmethod
    def date_data(date1, date2):
        s = {"$gt":date1}
        if date2 is not None:
            s["$gt"] = date2
        statement = {"date":s}

        return query.query(statement)
