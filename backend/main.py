from fastapi import FastAPI, UploadFile, File, Form
from typing import Dict
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI()

# 🧠 In-memory session history
chat_sessions: Dict[str, list] = {}

# -------------------------------
# 💬 Endpoint: Chat with memory
# -------------------------------
@app.post("/chat/")
async def chat(message: str = Form(...), language: str = Form(...), session_id: str = Form(...)):
    history = chat_sessions.get(session_id, [])
    history.append({"role": "user", "parts": [message]})

    try:
        response = model.generate_content(history)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    history.append({"role": "model", "parts": [reply]})
    chat_sessions[session_id] = history

    if language != "English":
        try:
            trans_prompt = f"Translate this to {language}:\n\n{reply}"
            trans_response = model.generate_content(trans_prompt)
            reply = trans_response.text.strip()
        except Exception as e:
            reply += f"\n\n(⚠️ Translation failed: {e})"

    return {"response": reply}

# -------------------------------------
# 📄 Endpoint: PDF Upload + Simplifier
# -------------------------------------
@app.post("/chat-pdf/")
async def chat_pdf(
    file: UploadFile = File(...),
    language: str = Form(...),
    session_id: str = Form(...)
):
    contents = await file.read()
    with open("temp.pdf", "wb") as f:
        f.write(contents)

    try:
        text = ""
        with fitz.open("temp.pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        return {"error": f"❌ Failed to read PDF: {e}"}
    finally:
        os.remove("temp.pdf")

    if not text.strip():
        return {"error": "❌ No extractable text found in PDF."}

    prompt = f"Please simplify this legal document:\n\n{text}"
    history = chat_sessions.get(session_id, [])
    history.append({"role": "user", "parts": [prompt]})

    try:
        response = model.generate_content(history)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    history.append({"role": "model", "parts": [reply]})
    chat_sessions[session_id] = history

    if language != "English":
        try:
            trans_prompt = f"Translate this to {language}:\n\n{reply}"
            trans_response = model.generate_content(trans_prompt)
            reply = trans_response.text.strip()
        except Exception as e:
            reply += f"\n\n(⚠️ Translation failed: {e})"

    return {"response": reply}
