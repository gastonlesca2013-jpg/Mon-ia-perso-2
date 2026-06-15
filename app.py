import streamlit as st
from openai import OpenAI # Nécessite : pip install openai

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS POUR UN DESIGN TOTALEMENT SOMBRE ET SANS SURVOL ---
st.markdown("""
    <style>
    /* Fond global */
    .stApp { background-color: #1a1a1a !important; }
    
    /* Barre latérale */
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Boutons : Couleur fixe, aucune animation au survol */
    div.stButton > button { 
        background-color: #262626 !important; 
        color: white !important; 
        border: 1px solid #444 !important; 
        transition: none !important; 
    }
    div.stButton > button:hover { background-color: #262626 !important; border: 1px solid #444 !important; }
    
    /* Supprimer les avatars (la petite tête) */
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

# --- INITIALISATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- AFFICHAGE DES BULLES (DESIGN GEMINI) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GESTION DE LA RÉPONSE RÉELLE ---
if prompt := st.chat_input("Demander à Kalyx..."):
    # Affichage utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Indicateur de réflexion (spinner)
    with st.chat_message("assistant"):
        with st.spinner('Kalyx réfléchit...'):
            # --- CONNECTEUR IA ---
            # Remplacez "VOTRE_API_KEY" par votre clé OpenAI ou autre
            try:
                client = OpenAI(api_key="VOTRE_API_KEY")
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                ).choices[0].message.content
            except:
                response = "Erreur : Veuillez configurer une clé API valide pour que je puisse répondre."
            
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
