import requests
import json

message =     [
        {"role": "user", "content": "I am going to Paris, what should I see?"},
    ]
res = requests.post(f"http://127.0.0.1:4396/",json={"message":message})
print(res.text)