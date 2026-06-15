import streamlit as st
import google.generativeai as genai

# 1. Configuration forcée du design (Texte blanc)
st.set_page_config(page_title="Kalyx", page_icon="🤖")
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    div[data-testid="stMarkdownContainer"], p, h1, h2, div { color: white !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Kalyx - Assistant")

# 2. Configuration de la clé API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Ajoutez GEMINI_API_KEY dans les secrets Streamlit !")
    st.stop()

# 3. Initialisation de la discussion
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Gestion de la question
if user_input := st.chat_input("Posez votre question..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        try:
            # Utilisation du modèle flash standard
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erreur : {e}")
