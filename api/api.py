from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collections.abc import Iterable
from db import add_one_document, add_many_document, query

app = FastAPI()
class Data(BaseModel):
    application_history: dict[str, int] | None
    screen_time: int = 0

class Behavior(BaseModel):
    date: datetime
    date_sent: datetime
    data: Data
    user: int
    
    def check_integrity(self):
        data = self.data
        if self.date is None or self.date_sent is None:
            raise HTTPException(404, "document's date does not exist")
        if data.application_history is None or sum(data.application_history.values()) != data.screen_time:
            raise HTTPException(404, "document's screen time does not line up with application history")
        return 0

class Behaviors(BaseModel):
    data:list[Behavior]

    def check_integrity(self):
        user = self.data[0].user
        for item in self.data:
            item.check_integrity()
            if item.user != user:
                raise HTTPException(404, "document sent multiple users at once, which is not allowed")

@app.post("/data/single/")
async def single_data(item:Behavior):
    item.check_integrity()
    add_one_document(item)
    return {"message":"document added successfully"}

@app.post("/data/multiple/")
async def multi_data(items:Behaviors):
    items.check_integrity()
    add_many_document(items)
    return {"message":"documents added successfully"}

@app.get("/data/query")
async def query_data(q):
    return query.query(q)

@app.get("/data/user")
async def user_data(user:int|Iterable):
    return query.user_data(user)

@app.get("/data/date")
async def date_data(date1:int, date2:int=None):
    return query.date_data(date1, date2)
