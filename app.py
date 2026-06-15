import streamlit as st
import google.generativeai as genai

# Configuration de l'API
genai.configure(api_key="VOTRE_CLE_API_ICI")

st.title("Kalyx Interface")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrée utilisateur
if prompt := st.chat_input("Demander à Kalyx"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appel au modèle
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
