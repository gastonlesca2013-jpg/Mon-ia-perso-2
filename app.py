import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Kalyx", layout="wide")

# --- INITIALISATION ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "bg_mode" not in st.session_state: st.session_state.bg_mode = "tropical"
if "current_view" not in st.session_state: st.session_state.current_view = "chat"

# --- CSS POUR COUVRIR TOUT L'ÉCRAN ---
BG_TROPICAL = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
BG_JUL = "https://static.skyrock.fm/static/0.skyrock.fm/art/pic.99965315.2.jpg"
current_bg = BG_TROPICAL if st.session_state.bg_mode == "tropical" else BG_JUL

st.markdown(f"""
    <style>
    /* Fond d'écran global */
    .stApp {{
        background: url("{current_bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        height: 100vh;
    }}
    /* Correction pour que la barre de tâche soit bien visible */
    [data-testid="stSidebar"] {{ background-color: rgba(20, 20, 20, 0.8); }}
    </style>
""", unsafe_allow_html=True)

# --- PAGE DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("Connexion à Kalyx")
    user_email = st.text_input("Email")
    if st.button("Se connecter"):
        st.session_state.logged_in = True
        st.rerun()
    st.stop()

# --- SIDEBAR GAUCHE (Navigation) ---
with st.sidebar:
    # Logo + Nom
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=40)
    with col2:
        st.markdown("### Kalyx")
    
    st.divider()
    if st.button("➕ Nouvelle Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.text_input("🔍 Rechercher")
    
    if st.button("🖼️ Mes Images", use_container_width=True):
        st.session_state.current_view = "images"
    
    st.divider()
    st.subheader("Compte")
    st.button("📊 Activité", use_container_width=True)
    st.button("⚙️ Paramètres", use_container_width=True)
    st.write("👤 Profil: Connecté")

# --- LAYOUT PRINCIPAL (Chat + Barre Droite) ---
col_main, col_right = st.columns([4, 1])

with col_main:
    st.header("Kalyx vous écoute")
    
    # Logique de Chat
    if st.session_state.current_view == "chat":
        # API IA
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Affichage messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Votre message..."):
            # Commande Boom
            if "boom" in prompt.lower():
                st.session_state.bg_mode = "jul" if st.session_state.bg_mode == "tropical" else "tropical"
                st.rerun()
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("Erreur de réponse de l'IA.")

    # Logique Génération Image
    elif st.session_state.current_view == "images":
        st.subheader("Générateur d'images")
        img_prompt = st.text_input("Que voulez-vous créer ?")
        if st.button("Générer"):
            st.info(f"Génération de : {img_prompt}...")
            # Ici ajouter votre logique d'API d'image

# --- SIDEBAR DROITE (Infos) ---
with col_right:
    st.markdown("### ℹ️ Infos")
    st.write(f"Date: {datetime.now().strftime('%d/%m/%Y')}")
    st.write("Status: Actif")
    st.divider()
    st.write("Discussions récentes:")
    st.write("1. Projet Python")
    st.write("2. Aide IA")
