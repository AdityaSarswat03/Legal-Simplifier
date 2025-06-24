# 📄 Legal Simplifier

**Legal Simplifier** is a powerful AI-based web app that simplifies complex legal clauses and documents into plain, understandable language. It supports multilingual output, PDF uploads, and chat-based interactions with memory to allow natural follow-up questions — all powered by the **Gemini API** and built using **FastAPI + Streamlit**.

---

## 🚀 Features

- 🧠 **Conversational AI** – Ask legal questions or paste clauses, and get simplified responses.
- 🗃️ **PDF Upload Support** – Upload full legal documents in PDF format for simplification.
- 🌍 **Multilingual Output** – Get simplified results in multiple languages (English, Hindi, French, etc.).
- 💬 **Chat-style UI** – Talk to the AI like a chatbot with chat bubbles.
- 🧾 **Context Memory** – Follow-up questions use your previous messages (within the same session).
- 🖥️ **Full Stack** – Built with FastAPI (backend) and Streamlit (frontend).
- 🔐 **Environment-secure** – Uses `.env` for securely managing the Gemini API key.

---

## 📁 Project Structure

legal-simplifier/
│
├── backend/
│ ├── main.py # FastAPI backend with PDF & chat endpoints
│ └── requirements.txt # Backend dependencies
│
├── frontend/
│ └── app.py # Streamlit UI for chat + PDF + multilingual support
│
├── .env # (not committed) Contains GEMINI_API_KEY
├── .gitignore # Ignore temp files, virtual env, etc.
├── README.md # Project documentation
└── requirements.txt # Combined requirements (optional)


## 📦 Installation & Setup

### 1. Clone the Repo
git clone https://github.com/AdityaSarswat03/legal-simplifier.git


2. Create Virtual Environment
- python -m venv venv
- source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install Dependencies
- pip install -r backend/requirements.txt
- pip install streamlit requests python-dotenv

4. Set Up Environment Variables
- Create a .env file in the root with:
- GEMINI_API_KEY=your_google_gemini_api_key_here


▶️ Running the App
1. Start FastAPI Backend
- uvicorn backend.main:app --reload
- This will start the backend at http://127.0.0.1:8000.

2. Start Streamlit Frontend
- In another terminal:
- streamlit run frontend/app.py

         The app will open in your browser.