import streamlit as st
import time

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS POUR UNIFORMISER ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Boutons sidebar */
    div.stButton > button { background-color: #262626 !important; color: white !important; border: 1px solid #444 !important; }
    
    /* Zone de saisie */
    [data-testid="stChatInput"] { background-color: #262626 !important; border: 1px solid #444 !important; }
    
    /* Suppression des avatars (les petites têtes hideuses) */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.button("📄 Nouveau notebook", use_container_width=True)

# --- INITIALISATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AFFICHAGE ---
for message in st.session_state.messages:
    # On affiche sans utiliser st.chat_message pour éviter les avatars
    st.write(f"**{message['role'].capitalize()}:** {message['content']}")

# --- GESTION RAPIDE ---
if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.write(f"**User:** {prompt}")

    # Indicateur de chargement (l'œil ou rond qui tourne)
    with st.spinner('Kalyx cherche...'):
        # Ici, vous pouvez remplacer la simulation par l'appel réel à votre IA
        time.sleep(1) # Simulation de latence réduite
        response = "Réponse directe et rapide ici."
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.write(f"**Assistant:** {response}")
