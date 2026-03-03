import streamlit as st
import requests
import uuid

st.set_page_config(page_title="TalentScout | Hiring Assistant", page_icon="💼")

st.title("💼 TalentScout Hiring Assistant")
st.markdown("Welcome! I'm here to help with your initial application process.")


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm the TalentScout assistant. To get started, could you please tell me your full name and what position you're applying for?"}
    ]


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message here..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "message": prompt,
            "thread_id": st.session_state.thread_id
        }
        response = requests.post("http://localhost:8000/chat", json=payload)
        response.raise_for_status()
        data = response.json()

        with st.chat_message("assistant"):
            st.markdown(data["response"])
            st.session_state.messages.append({"role": "assistant", "content": data["response"]})
            
        with st.sidebar:
            st.header("Application Progress")
            st.json(data["data"])
            
    except Exception as e:
        st.error(f"Error connecting to backend: {e}")


if any(keyword in prompt.lower() for keyword in ["exit", "bye", "quit"]) if prompt else False:
    st.balloons()
    st.success("Conversation ended. Thank you for your time!")
    st.stop()

