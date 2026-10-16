
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="PurpleAI | Groq Chatbot",
    page_icon="💜",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e103b, #51218a, #241044);
        color: white;
    }
    h1, h2, p, label {
        color: #ffffff !important;
    }
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.09);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 16px;
    }
    [data-testid="stChatInput"] {
        border: 1px solid #a78bfa;
        border-radius: 14px;
    }
    .stButton button {
        background: #8b5cf6;
        color: white;
        border-radius: 12px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💜 PurpleAI")
st.caption("✨ Your intelligent AI companion, powered by Groq")

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

with st.sidebar:
    st.header("⚙️ Settings")
    st.write(f"🧠 Model: `{model}`")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.error("🔑 GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey! 👋 I'm PurpleAI. What would you like to explore today?",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="💜" if message["role"] == "assistant" else "🧑",
    ):
        st.markdown(message["content"])

if prompt := st.chat_input("✨ Ask me anything..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💜"):
        try:
            with st.spinner("🪄 Thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are PurpleAI, a helpful and friendly AI assistant.",
                        },
                        *st.session_state.messages,
                    ],
                    temperature=0.7,
                    max_tokens=512,
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as error:
            st.error(f"⚠️ Groq API error: {error}")
