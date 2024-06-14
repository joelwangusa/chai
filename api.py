from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Dict
from .service import create_bot_config, run_sequence, generate_summary, get_chat_history

# Initialize FastAPI
app = FastAPI()

# Define the request model for chat
class ChatRequest(BaseModel):
    input_text: str
    chat_history: List[Dict[str, str]]

# Define the response model for chat
class ChatResponse(BaseModel):
    response: str

# Define the request model for summary
class SummaryRequest(BaseModel):
    chat_history: List[Dict[str, str]]

# Define the response model for conversation summary
class SummaryResponse(BaseModel):
    summary: str

# Endpoint to receive a new chat message
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        # Create a default bot configuration
        bot_config = create_bot_config("User", "Bot", "I am Bot, and this is my mind.")
        # Use the provided chat history
        result = run_sequence(bot_config, request.input_text, request.chat_history)
        return ChatResponse(response=result["response"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define the response model for chat history
class ChatHistoryResponse(BaseModel):
    chat_history: List[Dict[str, str]]

# Endpoint to get chat history with pagination
@app.get("/chat_history", response_model=ChatHistoryResponse)
def chat_history_endpoint(page: int = Query(0, ge=0), size: int = Query(10, gt=0)):
    try:
        bot_config = create_bot_config("User", "Bot", "I am Bot, and this is my mind.")
        history = get_chat_history(bot_config, page, size)
        return ChatHistoryResponse(chat_history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST endpoint to get the summary of the conversation
@app.post("/summary", response_model=SummaryResponse)
def summary_endpoint(request: SummaryRequest = Body(...)):
    try:
        summary = generate_summary(request.chat_history)
        return SummaryResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
