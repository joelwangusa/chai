import requests
from functools import lru_cache
from typing_extensions import Annotated

#from . import config

@lru_cache
def get_settings():
    return config.Settings()


payload = {
    "memory": "I am Bot, and this is my mind.",
    "prompt": "An engaging conversation with Bot.",
    "bot_name": "Chai Bot",
    "user_name": "John Doe",
    "chat_history":
        [
          {"sender": "Bot", "message": "Hi there"},
          {"sender": "User", "message": "Hey Bot!"}
        ]
}

headers = {"Authorization": "Bearer CR_6700b8e747434541924772becb8fa85a"}

url = "http://127.0.0.1/chai_api/"
url = "https://guanaco-submitter.chai-research.com/endpoints/onsite/chat"


response = requests.post(url, json=payload, headers=headers)

print(response.json())

def send_message(message: str, ):
    pass