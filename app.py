import streamlit as st
import google.generativeai as genai

# Configuration du design pour la lisibilité
st.set_page_config(page_title="Kalyx", page_icon="🤖")
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    div[data-testid="stMarkdownContainer"], p, h1, div { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Kalyx est prêt")

# Configuration de la clé API (Vérifiez qu'elle est bien dans vos Secrets Streamlit)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Clé API manquante dans les Secrets.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Gestion de la question
if user_input := st.chat_input("Posez votre question..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        try:
            # Utilisation du modèle confirmé par votre diagnostic
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur technique : {e}")
