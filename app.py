import streamlit as st
import google.generativeai as genai
from streamlit_webrtc import webrtc_streamer
from streamlit_mic_recorder import mic_recorder
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Kalyx - Monia", page_icon="🌴", layout="wide")

# --- INITIALISATION ---
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
        if email and password:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Veuillez remplir les champs.")
    st.stop()

# --- 2. INTERFACE PRINCIPALE ---
# CSS pour le fond d'écran
bg_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1353&q=80"
st.markdown(f"""
    <style>
    .stApp {{ background: url("{bg_url}"); background-size: cover; background-attachment: fixed; }}
    </style>
""", unsafe_allow_html=True)

# Barre Latérale Gauche
with st.sidebar:
    st.title("Menu Kalyx")
    if st.button("➕ Nouvelle Discussion"):
        st.session_state.messages = []
        st.rerun()
    st.button("🖼️ Générer Image")
    st.divider()
    # Bouton Visio
    if st.button("🎥 Lancer Visio avec Monia"):
        st.session_state.visio_mode = not st.session_state.visio_mode
        st.rerun()

# --- GESTION DES COLONNES (SÉCURISÉE) ---
col_right = None 
if st.session_state.show_right_bar:
    col_main, col_right = st.columns([3, 1])
else:
    col_main = st.columns([1])[0]

# --- CONTENU PRINCIPAL ---
with col_main:
    # Mode Visio activé
    if st.session_state.visio_mode:
        st.warning("📞 En ligne avec Monia - Mode Visio Actif")
        webrtc_streamer(key="visio_camera")
        st.write("Monia vous écoute en temps réel...")
    else:
        st.title("🤖 Monia est prête")

    # Configuration IA
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Affichage des messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrée (Micro + Saisie)
    c_mic, c_input = st.columns([0.1, 0.9])
    with c_mic:
        audio = mic_recorder(start_prompt="🎙️", stop_prompt="⏹️", key='mic')
    with c_input:
        user_input = st.chat_input("Posez votre question à Monia...")

    # Traitement
    final_input = audio["text"] if audio and "text" in audio else user_input
    if final_input:
        st.session_state.messages.append({"role": "user", "content": final_input})
        with st.chat_message("user"):
            st.markdown(final_input)
        
        with st.chat_message("assistant"):
            # En mode visio, on force une réponse immédiate
            response = model.generate_content(final_input)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- BARRE D'INFORMATIONS (DROITE) ---
if col_right:
    with col_right:
        if st.button("↔️ Fermer Infos"):
            st.session_state.show_right_bar = False
            st.rerun()
        st.markdown("### 📅 Aujourd'hui")
        st.write(f"**Date :** {datetime.now().strftime('%d/%m/%Y')}")
        st.write(f"**Heure :** {datetime.now().strftime('%H:%M')}")
        st.info("Système Kalyx opérationnel.")
        st.write("• État : Connecté")
        st.write("• Réseau : Stable")
else:
    # Si fermée, on affiche un petit bouton pour l'ouvrir
    if st.button("↔️ Infos du Jour"):
        st.session_state.show_right_bar = True
        st.rerun()
