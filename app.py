import streamlit as st
import google.generativeai as genai
import os

# 1. Configuration de la page (Doit être en premier)
st.set_page_config(page_title="Gropi AI", page_icon="🧠")
st.title("🧠 Gropi AI")

# 2. Configuration API (Utilise les secrets pour la sécurité)
# Si tu n'as pas encore mis les secrets, remplace os.environ par ta clé entre guillemets
api_key = st.secrets.get("API_KEY", "TA_CLE_API_ICI")
genai.configure(api_key=api_key)

# 3. Initialisation du modèle
model = genai.GenerativeModel('gemini-pro')

# 4. Gestion de l'état de la session (Historique)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Zone de saisie (La logique de chat va ici, en bas)
if prompt := st.chat_input("Pose ta question à Gropi..."):
    # Affiche le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    try:
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
