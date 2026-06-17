import streamlit as st
import google.generativeai as genai
from streamlit_webrtc import webrtc_streamer

# Configuration
st.set_page_config(page_title="Kalyx", page_icon="🌴", layout="wide")

# Initialisation des états
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "messages" not in st.session_state: st.session_state.messages = []
if "show_right_bar" not in st.session_state: st.session_state.show_right_bar = True
if "visio_mode" not in st.session_state: st.session_state.visio_mode = False

# --- 1. PORTAIL DE CONNEXION ---
if not st.session_state.logged_in:
    st.title("🔒 Connexion à Kalyx")
    email = st.text_input("Adresse Email")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if email and password: # Ajoutez ici votre logique de validation réelle
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Veuillez remplir tous les champs")
    st.stop() # Arrête le script ici si non connecté

# --- 2. INTERFACE PRINCIPALE (Si connecté) ---
# Fond d'écran
bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"
st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg_url}"); background-size: cover; background-attachment: fixed; }}
    </style>
""", unsafe_allow_html=True)

# Barre Latérale
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")
    st.divider()
    
    # Toggle Visio
    if st.button("🎥 Activer/Désactiver Visio"):
        st.session_state.visio_mode = not st.session_state.visio_mode
        st.rerun()
    
    search = st.text_input("🔍 Recherche")

# Mise en page
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]

with col_main:
    st.title("🤖 Kalyx")
    
    # Mode Visio (Accès Caméra)
    if st.session_state.visio_mode:
        st.info("Mode Visio activé. Veuillez autoriser l'accès à votre caméra.")
        webrtc_streamer(key="visio_camera")
        st.write("Kalyx est en mode visio avec vous.")

    # Chat
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-2.5-flash")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Posez votre question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("assistant"):
            response = model.generate_content(user_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# Barre Droite
with col_right:
    if st.button("↔️ Informations"):
        st.session_state.show_right_bar = not st.session_state.show_right_bar
        st.rerun()
    if st.session_state.show_right_bar:
        st.markdown("### ℹ️ Informations")
        st.write("• Système en ligne")
        st.write("• Utilisateur connecté")
