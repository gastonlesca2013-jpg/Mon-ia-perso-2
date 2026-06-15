import streamlit as st
from openai import OpenAI

# Configuration
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS (Design sobre et sombre) ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    div.stButton > button { background-color: #262626 !important; color: white !important; border: 1px solid #444 !important; transition: none !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    .stChatMessageContent { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# Barre latérale
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Initialisation de l'IA
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tentative de connexion
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("Clé API introuvable dans les secrets.")
    st.stop()

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie
if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Kalyx cherche la réponse...'):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "m", "content": m["content"]} for m in st.session_state.messages]
                ).choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erreur technique : {e}")
