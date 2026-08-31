from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GlucoSense AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nanti diganti URL Vercel
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def health_check():
    return {"status": "GlucoSense AI Service is running"}


@app.post("/chat/")
def chat(request: ChatRequest):
    from rag import get_response
    result = get_response(request.message)
    return result