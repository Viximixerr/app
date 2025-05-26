from datetime import datetime
import asyncio
import requests
import json
from data_collection import collect_data

url = "url"
user = 12312
lim = 5
send_list = []
checkpoint_dir = ""

class Counter():
    def __init__(self):
        self.send_time = datetime.now()

    async def update_date(self):
        asyncio.sleep(3600)
        self.send_time = datetime.now()
    
    def relinquish(self):
        del self

    def __call__(self):
        return self.send_time

async def send_to_api(current_data):
    now = datetime.now()
    current_data["date_sent"] = now
    current_data["user"] = user

    if len(send_list)==0:
        target = url + "/data/single/"
        data = current_data
    else:
        for i in range(len(send_list)):
            send_list[i]["date_sent"] = now
        target = url + "/data/multiple/"
        p = send_list + [current_data]
        data = {"data":p}
    
    open('test.json', 'w').write(json.dumps(data))
    with open('test.json', 'r') as f:
        data = json.load(f)
        r = requests.post(target, json=data)

    if r.status_code == 200:
        print("sent the package successfully \n")
        send_list = []
    else:
        print("fail to send the package")
        send_list.append(current_data)

    if len(send_list)>lim:
        with f as open(checkpoint_dir+"/checkpoint.json", "w"):
            f.write(json.dumps(data))
        print("warning: send list is over the limit, something wrong with the network or server we are so done lmao")

async def package():
    data_task = asyncio.create_task(collect_data())
    await data_task
    await send_to_api(data_task.result())

if __name__ == "__main__":
    while True:
        asyncio.run(package())
