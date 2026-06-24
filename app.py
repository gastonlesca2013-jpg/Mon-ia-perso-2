import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Gropi AI", page_icon="🧠")
st.title("🧠 Gropi AI")

# Configuration de l'API (Remplace par ta vraie clé)
# Dans un projet réel, utilise st.secrets pour la sécurité !
genai.configure(api_key="TA_CLE_API_ICI")

# Initialisation du modèle
model = genai.GenerativeModel('gemini-pro')

# Gestion de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages passés
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Pose ta question à Gropi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        full_response = response.text
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
