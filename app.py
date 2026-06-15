import streamlit as st

# Configuration de la page
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

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🟪 Kalyx")
    if st.button("➕ Nouvelle discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.button("📄 Nouveau notebook", use_container_width=True)
    st.markdown("<br><p style='color: gray; font-size: 0.8em;'>Récents</p>", unsafe_allow_html=True)
    st.button("• Achat Lamborghini", use_container_width=True)

# --- LOGIQUE SANS CLÉ API (Gratuit et immédiat) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Saisie utilisateur
if prompt := st.chat_input("Demander à Kalyx..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse simulée intelligente (sans clé API)
    with st.chat_message("assistant"):
        with st.spinner('Kalyx réfléchit...'):
            # Ici, Kalyx répond en fonction du texte saisi
            if "lamborghini" in prompt.lower():
                reponse = "Une Lamborghini neuve coûte généralement entre 250 000 € et 500 000 € selon le modèle (Urus, Huracán, Revuelto)."
            elif "bonjour" in prompt.lower():
                reponse = "Bonjour ! Je suis Kalyx, votre assistant personnel. Comment puis-je vous aider aujourd'hui ?"
            else:
                reponse = f"J'ai bien noté votre demande concernant : '{prompt}'. En tant qu'IA locale, je suis prêt à vous aider."
            
            st.markdown(reponse)
    
    st.session_state.messages.append({"role": "assistant", "content": reponse})
