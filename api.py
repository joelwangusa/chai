import os
from functools import lru_cache
from typing_extensions import Annotated

from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from . import config
from pydantic import BaseModel
from .service import run_sequence


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
    user_name: str
    bot_name: str
    memory: str
    chat_history: list
    input_text: str

# Define the response model
class ChatResponse(BaseModel):
    response: str

# Endpoint to receive a new chat message
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        # Convert chat history to string format
        chat_history_str = "\n".join(f"{msg['sender']}: {msg['message']}" for msg in request.chat_history)
        
        # Run the sequence with the incoming message
        result = run_sequence({
            "user_name": request.user_name,
            "bot_name": request.bot_name,
            "memory": request.memory,
            "chat_history": chat_history_str,
            "input_text": request.input_text
        })
        
        return ChatResponse(response=result["response"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)