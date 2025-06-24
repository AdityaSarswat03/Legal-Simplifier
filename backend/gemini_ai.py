import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")  

def simplify_text(clause: str) -> str:
    prompt = f"Simplify the following legal clause in plain English:\n\n{clause}"
    response = model.generate_content(prompt)
    return response.text.strip()
