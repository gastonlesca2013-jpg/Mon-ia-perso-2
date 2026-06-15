import streamlit as st
from openai import OpenAI

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS PERSONNALISÉ (Identique au design recherché) ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Boutons fixes, sans animation bizarre */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: 1px solid #444 !important; 
        transition: none !important; 
    }
    div.stButton > button:hover { border: 1px solid #7b2cbf !important; }
    
    /* Suppression totale des avatars */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    
    /* Texte blanc lisible */
    .stChatMessageContent { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• Achat Lamborghini", use_container_width=True)

# --- INITIALISATION IA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vérification sécurisée de la clé API
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("Erreur : La clé API n'est pas configurée dans les 'Secrets' Streamlit.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- AFFICHAGE DES MESSAGES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GESTION DE LA SAISIE ---
if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Kalyx analyse votre demande...'):
            try:
                response_stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                )
                response = response_stream.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("Une erreur est survenue lors de la recherche.")
