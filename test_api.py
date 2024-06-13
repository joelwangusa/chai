import pytest
from fastapi.testclient import TestClient
from .api import app

# Initialize the TestClient with our FastAPI app
client = TestClient(app)

# Test case for the /chat endpoint
def test_chat_endpoint():
    response = client.post("/chat", json={"input_text": "Hello, Bot!"})
    assert response.status_code == 200
    assert "response" in response.json()

# Test case for the /chat_history endpoint
def test_chat_history_endpoint():
    # First, send a few chat messages to populate the history
    client.post("/chat", json={"input_text": "Hello, Bot!"})
    client.post("/chat", json={"input_text": "How are you, Bot?"})

    # Now, fetch the chat history
    response = client.get("/chat_history?page=0&size=5")
    assert response.status_code == 200
    history = response.json()
    assert "chat_history" in history
    assert len(history["chat_history"]) > 0

# Test case for pagination in the /chat_history endpoint
def test_chat_history_pagination():
    # Send multiple chat messages to create a longer history
    for i in range(10):
        client.post("/chat", json={"input_text": f"Message {i}"})

    # Fetch the first page of the chat history
    response = client.get("/chat_history?page=0&size=5")
    assert response.status_code == 200
    history_page_1 = response.json()["chat_history"]
    assert len(history_page_1) == 5

    # Fetch the second page of the chat history
    response = client.get("/chat_history?page=1&size=5")
    assert response.status_code == 200
    history_page_2 = response.json()["chat_history"]
    assert len(history_page_2) == 5

    # Ensure no overlap between pages
    assert history_page_1 != history_page_2
