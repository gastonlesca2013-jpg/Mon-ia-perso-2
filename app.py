import streamlit as st
from openai import OpenAI

# Configuration
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS (Design sombre et épuré) ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    div.stButton > button { background-color: #262626 !important; color: white !important; border: 1px solid #444 !important; transition: none !important; }
    div.stButton > button:hover { border: 1px solid #7b2cbf !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    .stChatMessageContent { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Boutons activés) ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• Achat Lamborghini", use_container_width=True)

# --- LOGIQUE D'IA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialiser le client OpenAI (nécessite une clé API)
# Vous devez définir votre clé dans les "Secrets" de Streamlit Cloud
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Kalyx analyse votre demande...'):
            # Appel à l'IA pour obtenir une VRAIE réponse
            response_stream = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )
            response = response_stream.choices[0].message.content
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
