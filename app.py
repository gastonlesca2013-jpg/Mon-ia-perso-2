import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS POUR UN DESIGN PRO (Sombre, sans survol, sans avatars) ---
st.markdown("""
    <style>
    /* Fond principal sombre */
    .stApp { background-color: #1a1a1a !important; }
    
    /* Sidebar sombre */
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Boutons : Fixes, pas d'effet gris au survol */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: 1px solid #444 !important; 
        transition: none !important; 
    }
    div.stButton > button:hover { background-color: #262626 !important; border: 1px solid #444 !important; }
    
    /* Supprimer les avatars des bulles */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }
    
    /* Texte blanc */
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
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- INITIALISATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AFFICHAGE DES BULLES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GESTION DE SAISIE ---
if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner('Kalyx cherche...'):
            # Simulation de réponse : Remplacez par votre logique IA
            response = "Je suis Kalyx, comment puis-je vous aider aujourd'hui ?"
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
