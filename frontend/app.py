import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.title("JARVIS Chat")

# Historique conserve pendant la session Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Affiche tout l'historique deja present
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Champ de saisie utilisateur
user_input = st.chat_input("Ask something...")
if user_input:
    # Ajoute le message utilisateur a l'historique
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Envoie tout l'historique au backend
    try:
        resp = requests.post(
            API_URL,
            json={"messages": st.session_state["messages"]},
            timeout=60,
        )
        resp.raise_for_status()
        reply = resp.json()["reply"]
    except requests.RequestException as exc:
        # Message simple si l'API ne repond pas
        reply = f"Request failed: {exc}"

    # Ajoute et affiche la reponse de l'IA
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
