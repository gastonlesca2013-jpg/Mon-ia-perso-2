import streamlit as st

# Configuration de la page
st.set_page_config(layout="wide", page_title="Kalyx")

# --- CSS POUR UNIFORMISER LE NOIR/GRIS SOMBRE ---
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a !important; }
    [data-testid="stSidebar"] { background-color: #121212 !important; border-right: 1px solid #333; }
    
    /* Boutons sidebar utilisables */
    div.stButton > button { background-color: #262626 !important; color: white !important; border: 1px solid #444 !important; }
    div.stButton > button:hover { border: 1px solid #7b2cbf !important; }
    
    /* Zone de saisie */
    [data-testid="stChatInput"] { background-color: #262626 !important; border: 1px solid #444 !important; }
    </style>
""", unsafe_allow_html=True)

# --- LOGIQUE DE DISCUSSION (Pour avoir les bulles) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR (Barre de tâches utilisable) ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = [] # Réinitialise la conversation
        st.rerun()
    
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• achat casquettes", use_container_width=True)
    st.button("• bonjour", use_container_width=True)

# --- AFFICHAGE DES BULLES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GESTION DE LA SAISIE (Fonctionnelle) ---
if prompt := st.chat_input("Demander à Kalyx..."):
    # 1. Ajouter le message utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Réponse de l'IA (Simulation de rapidité)
    with st.chat_message("assistant"):
        response = f"Kalyx a bien reçu : '{prompt}'. Je traite votre demande..."
        st.markdown(response)
    
    # 3. Ajouter la réponse à l'historique
    st.session_state.messages.append({"role": "assistant", "content": response})
