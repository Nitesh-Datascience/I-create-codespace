
import os

import streamlit as st
from openai import OpenAI

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="PyBuddy AI",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 PyBuddy AI")
st.caption("Your beginner-friendly Python chatbot")

# -------------------------------
# AI configuration
# -------------------------------
api_key = (
    st.secrets.get("OPENAI_API_KEY", "")
    if "OPENAI_API_KEY" in st.secrets
    else os.getenv("OPENAI_API_KEY", "")
)

with st.sidebar:
    st.header("Settings")
    st.write("Choose how your chatbot responds.")

    mode = st.radio(
        "Chatbot mode",
        ["Demo mode", "AI mode"],
    )

    if mode == "AI mode" and not api_key:
        st.warning(
            "No API key found. Configure OPENAI_API_KEY "
            "to use real AI responses."
        )

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# -------------------------------
# Initialize conversation
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Demo response function
# -------------------------------
def demo_reply(prompt):
    text = prompt.lower()

    if "hello" in text or "hi" in text:
        return "Hello! 👋 I'm PyBuddy. How can I help you?"

    if "python" in text:
        return (
            "Python is a beginner-friendly programming "
            "language used in AI, automation, and data science."
        )

    if "your name" in text:
        return "I'm PyBuddy AI, your coding companion!"

    if "help" in text:
        return (
            "I can chat with you in demo mode. "
            "Switch to AI mode and configure an API key "
            "for more intelligent answers."
        )

    return (
        "That's interesting! I'm currently in demo mode. "
        "Connect an AI API to get more detailed answers."
    )

# -------------------------------
# Display previous messages
# -------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Handle new messages
# -------------------------------
prompt = st.chat_input("Ask PyBuddy something...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if mode == "AI mode" and api_key:
                client = OpenAI(api_key=api_key)

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are PyBuddy, a friendly AI "
                                "assistant. Explain concepts "
                                "clearly, especially for beginners."
                            ),
                        },
                        *st.session_state.messages[-12:],
                    ],
                )

                answer = response.choices[0].message.content
                answer = answer or "I couldn't generate a reply."

            elif mode == "AI mode":
                answer = (
                    "Please configure your OpenAI API key "
                    "in Codespaces, then restart the app."
                )

            else:
                answer = demo_reply(prompt)

        except Exception as error:
            answer = (
                "Sorry, I couldn't get a response. "
                "Check your API key, account access, "
                "internet connection, and API usage limits."
            )
            st.error(f"Error details: {error}")

        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
