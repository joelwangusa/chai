import pytest
from fastapi.testclient import TestClient
import sys
import os
import time

# Ensure the current directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .api import app

# Initialize the TestClient with our FastAPI app
client = TestClient(app)

def test_twobots():
    # Initial messages
    bot1_message = "Hello, nice to meeting you, Ben!"
    bot2_message = "Hey, nice to meeting you too, Joel!"

    # Number of exchanges
    exchanges = 5

    for i in range(exchanges):
        # Bot1 sends a message
        response1 = client.post("/chat", json={"input_text": bot1_message}, timeout=10)
        assert response1.status_code == 200
        bot2_message = response1.json()["response"]
        print(f"Bot2: {bot2_message}")

        # Simulate a delay
        time.sleep(1)

        # Bot2 sends a message
        response2 = client.post("/chat", json={"input_text": bot2_message}, timeout=10)
        assert response2.status_code == 200
        bot1_message = response2.json()["response"]
        print(f"Bot1: {bot1_message}")

        # Simulate a delay
        time.sleep(1)

if __name__ == "__main__":
    test_bot_conversation()
