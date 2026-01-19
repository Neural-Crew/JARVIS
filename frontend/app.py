import streamlit as st # pyright: ignore[reportMissingImports]
import requests

API_URL = "http://localhost:8000/chat"

def iter_chat_stream(messages, api_url=API_URL, requests_module=requests):
    with requests_module.post(api_url, json={"messages": messages}, stream=True) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                yield chunk

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

    with st.chat_message("assistant"):
        full_response = st.write_stream(
            iter_chat_stream(st.session_state["messages"])
        )
    
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

