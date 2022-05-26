from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from mongo import checkTOKEN
from inter import main

import uvicorn

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AI(BaseModel):
    AUTH_TOKEN: str
    DS_TOKEN: str
    CHANNEL: str
    USER: str
    DELAY: int



@app.post("/ai/")
async def create_item(model: AI):
    if checkTOKEN(model.AUTH_TOKEN)==True:
            main(model.DS_TOKEN, model.CHANNEL, model.USER, model.DELAY)
            return True
    else:
        return False


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")