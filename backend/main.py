# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import fitz
import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import Dict

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# 🧠 In-memory session-based history (clears when server restarts)
chat_sessions: Dict[str, list] = {}

# Simplify text with history support
@app.post("/chat/")
async def chat(message: str = Form(...), language: str = Form(...), session_id: str = Form(...)):
    history = chat_sessions.get(session_id, [])

    # Add latest message to history
    history.append({"role": "user", "parts": [message]})

    try:
        response = model.generate_content(history)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    # Add assistant response
    history.append({"role": "model", "parts": [reply]})
    chat_sessions[session_id] = history

    # Translate if needed
    if language != "English":
        try:
            trans_prompt = f"Translate this to {language}:\n\n{reply}"
            trans_response = model.generate_content(trans_prompt)
            reply = trans_response.text.strip()
        except Exception as e:
            reply += f"\n\n(⚠️ Translation failed: {e})"

    return {"response": reply}
