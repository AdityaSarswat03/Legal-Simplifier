import streamlit as st
import requests
import uuid

# Session ID for memory support
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page config
st.set_page_config(page_title="Legal Simplifier", layout="centered")

# Custom styling
st.markdown("""
    <style>
    html, body {
        background-color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextArea label, .stFileUploader label {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📄 Legal Simplifier")
st.caption("Turn legal clauses or full PDFs into plain language. 🌍 Multilingual output supported. 🧠 Ask follow-up questions in chat!")

# 🔁 Show previous messages (chat history)
for exchange in st.session_state.chat_history:
    st.chat_message("user").write(exchange["user"])
    st.chat_message("assistant").write(exchange["bot"])

# Language selection
language = st.selectbox("🌐 Choose output language", [
    "English", "Hindi", "Spanish", "French", "German", "Tamil", "Telugu", "Bengali"
])

# Input method selection
option = st.radio("✏️ Input Type", ["💬 Type Text", "📄 Upload PDF"])

# 💬 Text Chat Mode
if option == "💬 Type Text":
    user_input = st.chat_input("Type your legal clause or follow-up question...")

    if user_input:
        st.chat_message("user").write(user_input)

        with st.spinner("Simplifying..."):
            try:
                res = requests.post(
                    "https://legal-simplifier.onrender.com/chat/"
,
                    data={
                        "message": user_input,
                        "language": language,
                        "session_id": st.session_state.session_id
                    }
                )
                result = res.json()
                reply = result.get("response") or result.get("error", "❌ Something went wrong.")
            except Exception as e:
                reply = f"🚫 Connection error: {e}"

        st.chat_message("assistant").write(reply)
        st.session_state.chat_history.append({"user": user_input, "bot": reply})

# 📄 PDF Upload Mode
elif option == "📄 Upload PDF":
    uploaded_pdf = st.file_uploader("Upload your legal document (PDF)", type=["pdf"])

    if st.button("📄 Simplify PDF"):
        if uploaded_pdf:
            st.chat_message("user").write(f"📎 Uploaded PDF: {uploaded_pdf.name}")

            with st.spinner("Reading and simplifying PDF..."):
                try:
                    res = requests.post(
                        "https://legal-simplifier.onrender.com/chat-pdf/",
                        data={
                            "language": language,
                            "session_id": st.session_state.session_id
                        },
                        files={"file": uploaded_pdf}
                    )
                    result = res.json()
                    reply = result.get("response") or result.get("error", "❌ Something went wrong.")
                except Exception as e:
                    reply = f"🚫 Connection error: {e}"

            st.chat_message("assistant").write(reply)
            st.session_state.chat_history.append({"user": f"[PDF] {uploaded_pdf.name}", "bot": reply})
        else:
            st.warning("⚠️ Please upload a PDF first.")
