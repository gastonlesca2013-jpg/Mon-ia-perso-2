import streamlit as st
import google.generativeai as genai

# 1. Configurer l'IA (Utilise ta clé API ici ou via les Secrets de Streamlit)
genai.configure(api_key="TA_CLE_API_ICI")
model = genai.GenerativeModel(
    'gemini-pro',
    system_instruction="Tu es Gropi Études, un assistant expert en pédagogie. "
                       "Tu aides les étudiants à résumer des textes, créer des plans "
                       "de travail et expliquer des concepts complexes simplement."
)

# 2. Interface
st.set_page_config(page_title="Gropi Études", page_icon="📚")
st.title("📚 Gropi Études")

# Menu de choix dans la barre latérale
mode = st.sidebar.selectbox("Choisis ton mode :", ["Discussion", "Résumé de texte", "Explique-moi comme à 10 ans"])

# Historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie
if prompt := st.chat_input("Pose ta question..."):
    # Ajouter le contexte du mode choisi
    full_prompt = f"Mode {mode} : {prompt}" if mode != "Discussion" else prompt
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
    
    st.session_state.messages.append({"role": "assistant", "content": response.text})
