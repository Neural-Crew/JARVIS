import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.title("JARVIS Chat")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user_input = st.chat_input("Ask something...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        resp = requests.post(
            API_URL,
            json={"messages": st.session_state["messages"]},
            timeout=60,
        )
        resp.raise_for_status()
        reply = resp.json()["reply"]
    except requests.RequestException as exc:
        reply = f"Request failed: {exc}"

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
