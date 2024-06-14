import pytest
from fastapi.testclient import TestClient
from .api import app

# Initialize the TestClient with our FastAPI app
client = TestClient(app)

def test_chat():
    chat_history = []

    # Send the first message
    response = client.post("/chat", json={"input_text": "Hello, Bot!", "chat_history": chat_history})
    assert response.status_code == 200
    first_response = response.json()["response"]
    chat_history.append({"sender": "User", "message": "Hello, Bot!"})
    chat_history.append({"sender": "Bot", "message": first_response})

    # Check the response is not empty
    assert isinstance(first_response, str)
    assert len(first_response) > 0

    # Send the second message
    response = client.post("/chat", json={"input_text": "How are you today?", "chat_history": chat_history})
    assert response.status_code == 200
    second_response = response.json()["response"]
    chat_history.append({"sender": "User", "message": "How are you today?"})
    chat_history.append({"sender": "Bot", "message": second_response})

    # Check the response is not empty
    assert isinstance(second_response, str)
    assert len(second_response) > 0
    
    # Send the third message
    response = client.post("/chat", json={"input_text": "What can you do?", "chat_history": chat_history})
    assert response.status_code == 200
    third_response = response.json()["response"]
    chat_history.append({"sender": "User", "message": "What can you do?"})
    chat_history.append({"sender": "Bot", "message": third_response})

    # Check the response is not empty
    assert isinstance(third_response, str)
    assert len(third_response) > 0

# Sample chat history for testing
sample_chat_history = [
    {"sender": "User", "message": "Hello, Bot!"},
    {"sender": "User", "message": "How are you today?"},
    {"sender": "User", "message": "What can you do?"},
    {"sender": "User", "message": "That's cool."},
    {"sender": "User", "message": "Tell me a joke."},
]

def test_chat_history():
    chat_history = []

    # Submit chat messages
    for message in sample_chat_history:
        response = client.post("/chat", json={"input_text": message["message"], "chat_history": chat_history})
        assert response.status_code == 200
        bot_response = response.json()["response"]
        chat_history.append({"sender": "User", "message": message["message"]})
        chat_history.append({"sender": "Bot", "message": bot_response})

    response = client.get("/chat_history", params={"page": 0, "size": 5})
    assert response.status_code == 200
    result = response.json()
    assert len(result["chat_history"]) == 5


# Test case for the summary endpoint
def test_summary():
    chat_history = []

    # Submit chat messages
    for message in sample_chat_history:
        response = client.post("/chat", json={"input_text": message["message"], "chat_history": chat_history})
        assert response.status_code == 200
        bot_response = response.json()["response"]
        chat_history.append({"sender": "User", "message": message["message"]})
        chat_history.append({"sender": "Bot", "message": bot_response})
    
    # Request the summary of the conversation
    response = client.post("/summary", json={"chat_history": chat_history})
    
    assert response.status_code == 200
    summary = response.json()["summary"]

    assert isinstance(summary, str)
    assert len(summary) > 0
    print(summary)