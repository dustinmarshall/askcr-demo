"""
Simple AskCR Demo - A minimal ChatGPT-style web app.

This FastAPI application provides a streaming chat interface that proxies
requests to OpenAI's API and serves a simple web UI.
"""

import os
import json
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Data models
class ChatMessage(BaseModel):
    """Represents a single chat message."""
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    """Request payload for chat endpoint."""
    message: str
    messages: List[ChatMessage] = []

# API endpoints
@app.get("/")
async def root() -> FileResponse:
    """Serve the main web interface."""
    return FileResponse("static/index.html")


@app.post("/chat")
async def chat(req: ChatRequest):
    """
    Stream chat responses from OpenAI.
    
    Builds conversation context from message history and streams the response
    using Server-Sent Events format.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    try:
        client = OpenAI(api_key=api_key)
        
        # Build conversation context
        messages = [{"role": msg.role, "content": msg.content} for msg in req.messages]
        messages.append({"role": "user", "content": req.message})
        
        # Create streaming response
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
        
        def generate():
            try:
                # Stream content chunks
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
                
                # Signal completion
                yield f"data: {json.dumps({'done': True})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))