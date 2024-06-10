curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d '{
  "user_name": "User",
  "bot_name": "Bot",
  "memory": "I am Bot, and this is my mind.",
  "chat_history": [
    {"sender": "Bot", "message": "Hi there"},
    {"sender": "User", "message": "Hey Bot!"}
  ],
  "input_text": "What'\''s the weather like today?"
}'