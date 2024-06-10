import os
from functools import lru_cache
from typing_extensions import Annotated

from typing import Union

from fastapi import Depends, FastAPI
from . import config
from pydantic import BaseModel

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

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/chai_api/")
async def chai_api(item: MsgItem):
    message = item.message
    return {"message": message}