import os
from functools import lru_cache
from typing_extensions import Annotated

from typing import Union

from fastapi import Depends, FastAPI, HTTPException, Query
from . import config
from pydantic import BaseModel
from .service import run_sequence, get_chat_history


class MsgItem(BaseModel):
    message: str

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "chai_api_url": settings.chai_api_url
    }

# Define the request model
class ChatRequest(BaseModel):
    input_text: str

# Define the response model
class ChatResponse(BaseModel):
    response: str

# Define the response model for chat history
class ChatHistoryResponse(BaseModel):
    chat_history: list

# Endpoint to receive a new chat message
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        # Run the sequence with the incoming message
        result = run_sequence({
            "input_text": request.input_text,
            "chat_history": ""  # Placeholder, actual history managed in service
        })
        
        return ChatResponse(response=result["response"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to get chat history with pagination
@app.get("/chat_history", response_model=ChatHistoryResponse)
def chat_history_endpoint(page: int = Query(0, ge=0), size: int = Query(10, gt=0)):
    try:
        history = get_chat_history(page, size)
        return ChatHistoryResponse(chat_history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)