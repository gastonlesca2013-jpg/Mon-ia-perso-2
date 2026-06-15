import streamlit as st
from openai import OpenAI

st.set_page_config(layout="wide", page_title="Kalyx")

# CSS pour le design sombre
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

# Initialisation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vérification de la clé API
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Erreur : OPENAI_API_KEY non trouvée dans les paramètres Secrets.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Affichage historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie
if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Kalyx réfléchit...'):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                ).choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erreur API : {e}")
