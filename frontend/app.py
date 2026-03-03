import streamlit as st
import requests
import uuid
import os

# --- CONFIGURATION ---
# This looks for the BACKEND_URL provided by Render. 
# If it's not found (like when you run it on your laptop), it defaults to localhost.
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="TalentScout | Hiring Assistant", page_icon="💼")

st.title("💼 TalentScout Hiring Assistant")
st.markdown("Welcome! I'm here to help with your initial application process.")

# --- SESSION STATE ---
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm the TalentScout assistant. To get started, could you please tell me your full name and what position you're applying for?"}
    ]

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Type your message here..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "message": prompt,
            "thread_id": st.session_state.thread_id
        }
        
        # We use the dynamic BACKEND_URL here
        response = requests.post(f"{BACKEND_URL}/chat", json=payload)
        response.raise_for_status()
        data = response.json()

        # Display Assistant Response
        with st.chat_message("assistant"):
            st.markdown(data["response"])
            st.session_state.messages.append({"role": "assistant", "content": data["response"]})
            
        # Display Progress in Sidebar (Great for demonstrating the Agentic logic)
        with st.sidebar:
            st.header("📋 Application Data")
            st.write("This shows the data the AI has extracted so far:")
            st.json(data["data"])
            
    except Exception as e:
        st.error(f"⚠️ Connection Error: Could not reach the recruitment server.")
        st.info(f"Technical details: {e}")


# --- EXIT LOGIC ---
if prompt and any(keyword in prompt.lower() for keyword in ["exit", "bye", "quit"]):
    st.balloons()
    st.success("Conversation ended. Thank you for your time!")
    st.stop()