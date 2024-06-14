import pytest
from fastapi.testclient import TestClient
from .api import app

client = TestClient(app)

def test_summary_endpoint():
    # Simulate a conversation
    client.post("/chat", json={"input_text": "Hello, Bot!"})
    client.post("/chat", json={"input_text": "How are you today?"})
    client.post("/chat", json={"input_text": "What can you do?"})
    
    # Retrieve chat history
    response_history = client.get("/chat_history?page=0&size=10")
    assert response_history.status_code == 200
    chat_history = response_history.json()["chat_history"]
    
    # Request the summary of the conversation
    response = client.post("/summary", json={"chat_history": chat_history})
    
    assert response.status_code == 200
    summary = response.json()["summary"]
    
    assert isinstance(summary, str)
    assert len(summary) > 0
    print(summary)

if __name__ == "__main__":
    test_summary_endpoint()
