import pytest
from fastapi.testclient import TestClient
from .api import app
from .service import create_bot_config, run_sequence

client = TestClient(app)

def test_two_bots_chat():
    chat_history = []

    # Create bot configurations for two bots
    bot1_config = create_bot_config("Bot1User", "Bot1", "I am Bot1, and this is my mind.")
    bot2_config = create_bot_config("Bot2User", "Bot2", "I am Bot2, and this is my mind.")

    # Initial messages
    bot1_initial_message = "Hello, Bot2!"
    bot2_initial_message = "Hello, Bot1!"

    # Bot1 starts the conversation
    result = run_sequence(bot1_config, bot1_initial_message, chat_history)
    chat_history = result["chat_history"]

    # Continue the conversation for a few rounds
    for _ in range(5):
        # Bot2 responds to Bot1
        result = run_sequence(bot2_config, result["response"], chat_history)
        chat_history = result["chat_history"]
        response = result["response"]
        print(f"Bot2: {response}")

        # Bot1 responds to Bot2
        result = run_sequence(bot1_config, result["response"], chat_history)
        chat_history = result["chat_history"]
        response = result["response"]
        print(f"Bot1: {response}")

    # Verify the chat history length
    assert len(chat_history) > 0

    # Print the chat history for visual inspection
    for entry in chat_history:
        print(f"{entry['sender']}: {entry['message']}")

if __name__ == "__main__":
    test_two_bots_chat()
