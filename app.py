import streamlit as st
import google.generativeai as genai

# Design : Texte blanc forcé pour la lisibilité
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    div[data-testid="stMarkdownContainer"], p, h1, h2, div { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Kalyx")

# Vérification de la clé
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Clé GEMINI_API_KEY absente des secrets !")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Réponse
if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur de connexion : {e}")
