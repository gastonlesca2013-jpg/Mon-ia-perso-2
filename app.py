import streamlit as st
import time

# Configuration
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Texte blanc partout */
    div, p, h1, h2, h3, .stMarkdown { color: white !important; }
    
    /* Zone de saisie */
    [data-testid="stChatInput"] { background-color: #262626 !important; border: 1px solid #444 !important; }
    
    /* Supprimer les avatars */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
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
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- INITIALISATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- LOGIQUE D'AFFICHAGE ---
for message in st.session_state.messages:
    st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# --- SAISIE ET RÉPONSE ---
if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"**User:** {prompt}")

    # Animation de réflexion
    with st.spinner('Kalyx réfléchit...'):
        # --- ICI : REMPLACEZ CE BLOC PAR VOTRE APPEL D'API ---
        # Exemple pour une réponse réelle :
        # response = openai.ChatCompletion.create(...) 
        time.sleep(2) # Temps de réponse simulé
        response = "Voici la réponse réelle à votre question." 
        # ----------------------------------------------------
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f"**Assistant:** {response}")
    st.rerun()
