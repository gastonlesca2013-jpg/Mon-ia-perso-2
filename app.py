import streamlit as st
import google.generativeai as genai

# Configuration de la page
st.set_page_config(page_title="Kalyx", page_icon="🤖", layout="wide")

# --- 1. CONFIGURATION FOND D'ÉCRAN (Avec URL) ---
# Remplacez l'URL ci-dessous par le lien direct de votre image hébergée
bg_url = "VOTRE_URL_IMAGE_ICI" 

st.markdown(f"""
    <style>
    .stApp {{
        background: url("{bg_url}");
        background-size: cover;
        background-position: center;
    }}
    /* Rendre le fond du chat semi-transparent pour voir l'image derrière */
    [data-testid="stChatMessage"] {{
        background-color: rgba(0, 0, 0, 0.6) !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- INITIALISATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. BARRE LATÉRALE (Boutons fonctionnels) ---
with st.sidebar:
    st.title("Menu Kalyx")
    
    # Bouton Nouvelle Discussion
    if st.button("➕ Nouvelle Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Bouton Générer Image (Simulation)
    if st.button("🖼️ Générer une Image", use_container_width=True):
        st.warning("Fonctionnalité Image : En attente de connexion API.")
    
    st.divider()
    
    # Recherche fonctionnelle
    search = st.text_input("🔍 Rechercher dans les messages")
    if search:
        st.write(f"Résultats pour : {search}")
        for msg in st.session_state.messages:
            if search.lower() in msg["content"].lower():
                st.info(msg["content"][:30] + "...")

# --- 3. MISE EN PAGE ---
col_chat, col_news = st.columns([3, 1])

with col_chat:
    st.title("🤖 Kalyx est prêt")
    
    # Configuration API
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    else:
        st.error("Clé API manquante dans les Secrets.")
        st.stop()

    # Affichage Chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée utilisateur
    if user_input := st.chat_input("Posez votre question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 4. BARRE À DROITE (News) ---
with col_news:
    st.markdown("### 📰 Polymarquette")
    st.markdown("---")
    st.write("• ⚽ Paris : Matchs en direct")
    st.write("• 📈 Cotes : Mises à jour")
    st.write("• 🎁 Nouveau bonus disponible")
