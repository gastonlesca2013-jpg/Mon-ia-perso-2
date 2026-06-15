import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="💎", layout="centered")

# --- PERSONNALISATION DES COULEURS (STYLE LUXE SOMBRE) ---
st.markdown("""
    <style>
    /* Changer la couleur du fond général */
    .stApp {
        background-color: #0F1115;
    }
    /* Style du titre Kalyx */
    h1 {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: lowercase;
    }
    /* Couleur des textes saisis */
    .stChatMessage {
        background-color: #161920 !important;
        border-radius: 12px;
        border: 1px solid #232834;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("kalyx")

# Vérification de la clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante. Configure-la dans les paramètres de Streamlit.")
    st.stop()

# Historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone d'écriture et réponse
if user_input := st.chat_input("Pose-moi une question..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        try:
            # ICI : Passage au modèle mis à jour pour corriger l'erreur 404
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
