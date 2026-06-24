import streamlit as st
import google.generativeai as genai

# 1. Configuration de la page
st.set_page_config(page_title="Gropi Études", page_icon="📚")
st.title("📚 Gropi Études")

# 2. Configuration de l'API 
# Utilise ta clé générée sur Google AI Studio (commence par AIza)
genai.configure(api_key="TA_CLE_API_ICI")

# 3. Initialisation du modèle
model = genai.GenerativeModel('gemini-pro')

# 4. Gestion de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Zone de saisie
if prompt := st.chat_input("Pose ta question à Gropi..."):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
