from datetime import datetime
import requests
import json

now = str(datetime.now())
data ={
        "date":now,
        "date_sent":now,
        "data":{
            "application_history":{"geometry_dash":23},
            "screen_time":23
        },
        "user":0
    }

open('test.json', 'w').write(json.dumps(data))
with open('test.json', 'r') as f:
    data = json.load(f)
    # Make a POST request to the server
    requests.post('http://127.0.0.1:8000/post-irony/', json=data)

